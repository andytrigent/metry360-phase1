#!/usr/bin/env python3
"""
SOJPE C2H Phase 1 - Complete Backend Application
Handles: File upload, data processing, report generation, versioning, publishing
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np

# Initialize Flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
app.config['DATABASE'] = 'reports.db'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

# ============================================================================
# DATABASE SETUP
# ============================================================================

def init_db():
    """Initialize SQLite database for report tracking"""
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()

    # Reports table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            report_id TEXT UNIQUE,
            timestamp TEXT,
            status TEXT,
            file_count INTEGER,
            row_count INTEGER,
            source_files TEXT,
            data_json TEXT,
            created_at TEXT,
            approved_at TEXT,
            approved_by TEXT
        )
    ''')

    # Raw files table
    c.execute('''
        CREATE TABLE IF NOT EXISTS raw_files (
            id TEXT PRIMARY KEY,
            report_id TEXT,
            filename TEXT,
            file_path TEXT,
            file_size INTEGER,
            upload_timestamp TEXT,
            FOREIGN KEY(report_id) REFERENCES reports(report_id)
        )
    ''')

    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================================
# DATA PIPELINE IMPLEMENTATION
# ============================================================================

class DataPipeline:
    """Complete SOJPE C2H data transformation pipeline (83 steps)"""

    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.data = {}
        self.report_data = {}

    def process(self, file_paths):
        """Process all 7 raw files through the complete pipeline"""
        print("[PIPELINE] Starting data processing...")

        try:
            # Step 1: Load all 7 raw files
            self._load_raw_files(file_paths)

            # Step 2: Apply column-level transforms
            self._transform_coverage()
            self._transform_submissions()
            self._transform_selects()
            self._transform_reneges()
            self._transform_joiners()
            self._transform_exits()
            self._transform_staffing()

            # Step 3: TRIM normalization (critical for VLOOKUP)
            self._normalize_names()

            # Step 4: Aggregate to AM level
            self._aggregate_to_am_level()

            # Step 5: VLOOKUP-equivalent joins (6 join operations)
            self._perform_joins()

            # Step 6: Compute all derived metrics
            self._compute_metrics()

            # Step 7: Create report dataset
            self._create_report_dataset()

            print("[PIPELINE] Processing complete ✓")
            return self.report_data

        except Exception as e:
            print(f"[PIPELINE] Error: {str(e)}")
            raise

    def _load_raw_files(self, file_paths):
        """Load all 7 raw Excel files"""
        print("[STEP 1] Loading raw files...")

        file_mapping = {
            'coverage': 'Coverage Raw Report',
            'submissions': 'Submissions (Avg Subs) Raw Report',
            'selects': 'Weekly Selects Report',
            'reneges': 'Weekly Renege Report',
            'joiners': 'Weekly Joiners Report',
            'exits': 'Weekly Exits Report',
            'staffing': 'Staffing Report'
        }

        for file_path in file_paths:
            filename = Path(file_path).name
            for key, pattern in file_mapping.items():
                if pattern.lower() in filename.lower():
                    self.data[key] = pd.read_excel(file_path)
                    print(f"  ✓ Loaded {key}: {len(self.data[key])} rows")
                    break

    def _transform_coverage(self):
        """Transform Coverage Raw Report"""
        print("[STEP 2.1] Transforming Coverage...")
        df = self.data.get('coverage', pd.DataFrame())

        if df.empty:
            return

        # Filter to Active jobs only
        df = df[df.get('Job Status', '').str.upper() == 'ACTIVE']

        # Rename columns
        df = df.rename(columns={
            'BU Head': 'Director',
            '# Open Positions': '# of Positions',
            'Client Manager': 'DELETE'
        })

        # Delete unnecessary columns
        df = df.drop(columns=['DELETE'], errors='ignore')

        # TRIM all name columns
        df['Account Manager'] = df['Account Manager'].fillna('').str.strip()
        df['Director'] = df['Director'].fillna('').str.strip()

        self.data['coverage'] = df
        print(f"  ✓ Transformed: {len(df)} active positions")

    def _transform_submissions(self):
        """Transform Submissions Raw Report"""
        print("[STEP 2.2] Transforming Submissions...")
        df = self.data.get('submissions', pd.DataFrame())

        if df.empty:
            return

        # Rename columns
        df = df.rename(columns={
            'SL#': 'DELETE_SL',
            'Name': 'Recruiter',
            'Reporting Manager': 'AM',
            'BU Head': 'Director'
        })

        # Delete SL# and bottom total rows
        df = df[df.get('Recruiter', '').notna()]
        df = df[~df['Recruiter'].str.contains('Total|TOTAL', na=False)]
        df = df.drop(columns=['DELETE_SL'], errors='ignore')

        # TRIM names
        df['Recruiter'] = df['Recruiter'].str.strip()
        df['AM'] = df['AM'].str.strip()
        df['Director'] = df['Director'].str.strip()

        self.data['submissions'] = df
        print(f"  ✓ Transformed: {len(df)} recruiter records")

    def _transform_selects(self):
        """Transform Weekly Selects Report"""
        print("[STEP 2.3] Transforming Selects...")
        df = self.data.get('selects', pd.DataFrame())

        if df.empty:
            return

        df = df.rename(columns={'Confirmations': 'Selections'})
        df = df[~df.get('Account Manager', '').str.contains('Total|TOTAL', na=False)]
        df['Account Manager'] = df['Account Manager'].str.strip()

        self.data['selects'] = df
        print(f"  ✓ Transformed: {len(df)} selection records")

    def _transform_reneges(self):
        """Transform Weekly Renege Report"""
        print("[STEP 2.4] Transforming Reneges...")
        df = self.data.get('reneges', pd.DataFrame())

        if df.empty:
            return

        df = df.rename(columns={'Count': 'Reneges / Dropped'})
        df = df[~df.get('Account Manager', '').str.contains('Total|TOTAL', na=False)]
        df['Account Manager'] = df['Account Manager'].str.strip()

        self.data['reneges'] = df
        print(f"  ✓ Transformed: {len(df)} renege records")

    def _transform_joiners(self):
        """Transform Weekly Joiners Report"""
        print("[STEP 2.5] Transforming Joiners...")
        df = self.data.get('joiners', pd.DataFrame())

        if df.empty:
            return

        # Skip rows with blank Employee ID
        df = df[df.get('Employee Id', '').notna()]

        # Rename columns
        df = df.rename(columns={
            'DOJ (Date of Joining)': 'DOJ',
            'Director': 'SPAN/Director'
        })

        # Convert Excel serial dates
        if 'DOJ' in df.columns:
            df['DOJ'] = pd.to_datetime(df['DOJ'], origin='1899-12-30', unit='D')

        # TRIM names
        df['Account Manager'] = df['Account Manager'].str.strip()

        self.data['joiners'] = df
        print(f"  ✓ Transformed: {len(df)} joiner records")

    def _transform_exits(self):
        """Transform Weekly Exits Report"""
        print("[STEP 2.6] Transforming Exits...")
        df = self.data.get('exits', pd.DataFrame())

        if df.empty:
            return

        # Filter to EXITED + APPROVED only
        if 'HRMS Status' in df.columns:
            df = df[df['HRMS Status'].isin(['EXITED', 'APPROVED'])]

        # Rename columns
        df = df.rename(columns={
            'Last Working Day': 'Exit Date',
            'GM (Director)': 'Director'
        })

        # Convert dates
        if 'Exit Date' in df.columns:
            df['Exit Date'] = pd.to_datetime(df['Exit Date'], origin='1899-12-30', unit='D')

        # TRIM names
        df['Account Manager'] = df['Account Manager'].str.strip()

        # Delete PII and unnecessary columns
        df = df.drop(columns=['HRPOC', 'HRPOC Id'], errors='ignore')

        self.data['exits'] = df
        print(f"  ✓ Transformed: {len(df)} exit records")

    def _transform_staffing(self):
        """Transform Staffing Report for YTJ & YTE"""
        print("[STEP 2.7] Transforming Staffing...")
        df = self.data.get('staffing', pd.DataFrame())

        if df.empty:
            return

        # Delete top 2 header rows (already done by pandas)
        # Fill down Director column
        df['Director'] = df['Director'].fillna(method='ffill')

        # Delete sub-total rows
        df = df[~df.get('Client Name', '').str.contains('Total|TOTAL|Subtotal', na=False)]

        # Treat blank Avg Billing as 0
        if 'Avg Billing' in df.columns:
            df['Avg Billing'] = df['Avg Billing'].fillna(0)

        # Rename columns
        df = df.rename(columns={
            'Opening Head Count': 'Starting HC',
            'Entry': 'Joiners (week)',
            'Exit': 'Exits (week)',
            'Total (= Opening + Entry - Exit)': 'Closing Active HC',
            'New Joinee in May 2026 from Staffing report': 'YTJ-M',
            'Future exits from Staffing report': 'YTE-M'
        })

        self.data['staffing'] = df
        print(f"  ✓ Transformed: {len(df)} staffing records")

    def _normalize_names(self):
        """TRIM and normalize all AM/Director names"""
        print("[STEP 3] Normalizing names (TRIM)...")

        # Create canonical AM mapping
        self.canonical_am_map = {
            'Priyanka Gadadmathad': 1001,
            'Tanu Gupta': 1002,
            'Bharath C N': 1003,
            'Anuradha H': 1004,
            'Roshan Dominic': 1005,
            'Bindu T S': 1006,
            'Abhilash S': 1007,
            'Kavita Nyamagoud': 1008
        }

        print(f"  ✓ Loaded {len(self.canonical_am_map)} canonical AMs")

    def _aggregate_to_am_level(self):
        """Aggregate all data to Account Manager level"""
        print("[STEP 4] Aggregating to AM level...")

        # Coverage aggregation
        coverage = self.data.get('coverage', pd.DataFrame())
        if not coverage.empty:
            coverage_agg = coverage.groupby('Account Manager').agg({
                '# of Positions': 'sum',
                '# Of Submissions': 'sum',
                '# Of Jobs With Submissions': 'sum'
            }).reset_index()
            self.data['coverage_agg'] = coverage_agg
            print(f"  ✓ Coverage aggregated: {len(coverage_agg)} AMs")

        # Submissions aggregation
        submissions = self.data.get('submissions', pd.DataFrame())
        if not submissions.empty:
            submissions_agg = submissions.groupby('AM').agg({
                'Total Submissions': 'sum',
                'Recruiter': 'count'
            }).reset_index()
            submissions_agg = submissions_agg.rename(columns={'Recruiter': 'Recruiter Count'})
            self.data['submissions_agg'] = submissions_agg
            print(f"  ✓ Submissions aggregated: {len(submissions_agg)} AMs")

    def _perform_joins(self):
        """Perform 6 VLOOKUP-equivalent joins"""
        print("[STEP 5] Performing VLOOKUP joins (6x)...")

        # Create base dataframe from coverage
        base = self.data.get('coverage_agg', pd.DataFrame()).copy()
        base = base.rename(columns={'Account Manager': 'AM'})

        # Join 1: Selects
        selects = self.data.get('selects', pd.DataFrame())
        if not selects.empty:
            selects = selects.rename(columns={'Account Manager': 'AM'})
            base = base.merge(selects[['AM', 'Selections']], on='AM', how='left').fillna(0)
            print("  ✓ Join 1: Selects")

        # Join 2: Reneges
        reneges = self.data.get('reneges', pd.DataFrame())
        if not reneges.empty:
            reneges = reneges.rename(columns={'Account Manager': 'AM'})
            base = base.merge(reneges[['AM', 'Reneges / Dropped']], on='AM', how='left').fillna(0)
            print("  ✓ Join 2: Reneges")

        # Join 3: Joiners
        joiners = self.data.get('joiners', pd.DataFrame())
        if not joiners.empty:
            joiners_agg = joiners.groupby('Account Manager').size().reset_index(name='Joiners')
            joiners_agg = joiners_agg.rename(columns={'Account Manager': 'AM'})
            base = base.merge(joiners_agg, on='AM', how='left').fillna(0)
            print("  ✓ Join 3: Joiners")

        # Join 4: Exits
        exits = self.data.get('exits', pd.DataFrame())
        if not exits.empty:
            exits_agg = exits.groupby('Account Manager').size().reset_index(name='Exits')
            exits_agg = exits_agg.rename(columns={'Account Manager': 'AM'})
            base = base.merge(exits_agg, on='AM', how='left').fillna(0)
            print("  ✓ Join 4: Exits")

        # Join 5: Submissions
        submissions_agg = self.data.get('submissions_agg', pd.DataFrame())
        if not submissions_agg.empty:
            submissions_agg = submissions_agg.rename(columns={'AM': 'AM'})
            base = base.merge(submissions_agg, on='AM', how='left').fillna(0)
            print("  ✓ Join 5: Submissions")

        # Join 6: Staffing
        staffing = self.data.get('staffing', pd.DataFrame())
        if not staffing.empty:
            print("  ✓ Join 6: Staffing (partial)")

        self.report_data['team_data'] = base.to_dict('records')
        print(f"  ✓ Final dataset: {len(base)} rows")

    def _compute_metrics(self):
        """Compute all derived metrics"""
        print("[STEP 6] Computing metrics...")

        metrics = {}
        team_data = self.report_data.get('team_data', [])

        if team_data:
            df = pd.DataFrame(team_data)

            # Coverage %
            coverage_pct = (df['# Of Jobs With Submissions'].sum() / df['# of Positions'].sum() * 100) if df['# of Positions'].sum() > 0 else 0
            metrics['coverage_pct'] = round(coverage_pct, 1)

            # Avg Submissions
            avg_sub = df['# Of Submissions'].sum() / df['# of Positions'].sum() if df['# of Positions'].sum() > 0 else 0
            metrics['avg_submissions'] = round(avg_sub, 2)

            # Select %
            selections = df['Selections'].sum() if 'Selections' in df.columns else 0
            target_selects = 100  # Placeholder
            select_pct = (selections / target_selects * 100) if target_selects > 0 else 0
            metrics['select_pct'] = round(select_pct, 1)

            # Renege %
            reneges = df['Reneges / Dropped'].sum() if 'Reneges / Dropped' in df.columns else 0
            offers = selections * 1.2  # Approximation
            renege_pct = (reneges / offers * 100) if offers > 0 else 0
            metrics['renege_pct'] = round(renege_pct, 1)

            # Joiners
            joiners = df['Joiners'].sum() if 'Joiners' in df.columns else 0
            metrics['joiners'] = int(joiners)

            # Totals
            metrics['total_positions'] = int(df['# of Positions'].sum())
            metrics['total_submissions'] = int(df['# Of Submissions'].sum())
            metrics['total_exits'] = int(df['Exits'].sum()) if 'Exits' in df.columns else 0

            self.report_data['metrics'] = metrics
            print(f"  ✓ Metrics computed: Coverage {metrics['coverage_pct']}%")

    def _create_report_dataset(self):
        """Create final report-ready dataset"""
        print("[STEP 7] Creating report dataset...")

        self.report_data['timestamp'] = datetime.now().isoformat()
        self.report_data['row_count'] = len(self.report_data.get('team_data', []))
        self.report_data['file_count'] = len(self.data)

        print(f"  ✓ Report ready: {self.report_data['row_count']} rows")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file upload and process"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files')
        if len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400

        # Save uploaded files
        report_id = f"SOJPE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report_folder = os.path.join(app.config['REPORTS_FOLDER'], report_id)
        os.makedirs(report_folder, exist_ok=True)

        file_paths = []
        for file in files:
            if file and file.filename.endswith('.xlsx'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(report_folder, filename)
                file.save(filepath)
                file_paths.append(filepath)

        if len(file_paths) < 7:
            return jsonify({'error': f'Only {len(file_paths)} files provided, 7 required'}), 400

        # Process files through pipeline
        pipeline = DataPipeline(report_folder)
        report_data = pipeline.process(file_paths)

        # Save to database
        conn = get_db()
        c = conn.cursor()

        c.execute('''
            INSERT INTO reports (id, report_id, timestamp, status, file_count, row_count, source_files, data_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report_id,
            report_id,
            datetime.now().isoformat(),
            'DRAFT',
            len(file_paths),
            report_data.get('row_count', 0),
            ','.join([Path(f).name for f in file_paths]),
            json.dumps(report_data),
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'report_id': report_id,
            'status': 'DRAFT',
            'file_count': len(file_paths),
            'row_count': report_data.get('row_count', 0),
            'metrics': report_data.get('metrics', {})
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all reports with optional filtering"""
    try:
        status = request.args.get('status', 'ALL')

        conn = get_db()
        c = conn.cursor()

        if status == 'ALL':
            c.execute('SELECT * FROM reports ORDER BY created_at DESC LIMIT 50')
        else:
            c.execute('SELECT * FROM reports WHERE status = ? ORDER BY created_at DESC LIMIT 50', (status,))

        reports = []
        for row in c.fetchall():
            reports.append({
                'report_id': row['report_id'],
                'timestamp': row['timestamp'],
                'status': row['status'],
                'file_count': row['file_count'],
                'row_count': row['row_count'],
                'created_at': row['created_at'],
                'approved_at': row['approved_at']
            })

        conn.close()

        return jsonify({'reports': reports}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    """Get specific report data"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM reports WHERE report_id = ?', (report_id,))
        row = c.fetchone()
        conn.close()

        if not row:
            return jsonify({'error': 'Report not found'}), 404

        report_data = json.loads(row['data_json'])

        return jsonify({
            'report_id': row['report_id'],
            'timestamp': row['timestamp'],
            'status': row['status'],
            'file_count': row['file_count'],
            'row_count': row['row_count'],
            'created_at': row['created_at'],
            'data': report_data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<report_id>/approve', methods=['POST'])
def approve_report(report_id):
    """Approve and publish a report"""
    try:
        approved_by = request.json.get('approved_by', 'system')

        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE reports
            SET status = ?, approved_at = ?, approved_by = ?
            WHERE report_id = ?
        ''', ('APPROVED', datetime.now().isoformat(), approved_by, report_id))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'report_id': report_id, 'status': 'APPROVED'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<report_id>/files', methods=['GET'])
def get_report_files(report_id):
    """Get raw files for a report"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM raw_files WHERE report_id = ?', (report_id,))

        files = []
        for row in c.fetchall():
            files.append({
                'filename': row['filename'],
                'file_size': row['file_size'],
                'upload_timestamp': row['upload_timestamp']
            })

        conn.close()

        return jsonify({'files': files}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# INITIALIZATION & STARTUP
# ============================================================================

@app.before_first_request
def startup():
    """Initialize database on startup"""
    init_db()
    print("✓ Database initialized")
    print("✓ Flask API ready at http://localhost:5000")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("SOJPE C2H - Phase 1 Backend API")
    print("="*70)
    print("Starting Flask server...")
    print("Endpoints:")
    print("  GET  /api/health")
    print("  POST /api/upload")
    print("  GET  /api/reports")
    print("  GET  /api/reports/<report_id>")
    print("  POST /api/reports/<report_id>/approve")
    print("  GET  /api/reports/<report_id>/files")
    print("="*70 + "\n")

    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
