# SOJPE C2H Phase 1 — Weekly Reporting Automation

**Status:** Live in production (infrastructure verified end-to-end 2026-07-10) | **Org:** trigent-ark-os

## Live URLs

| URL | Purpose |
|-----|---------|
| https://metry360.arkos.studio | Production frontend (Vercel) |
| https://metry360.arkos.studio/dashboard.html | Dashboard |
| https://metry360.arkos.studio/upload-new.html | Upload the 7 weekly raw files |
| https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod | Backend API (AWS API Gateway → Lambda) |
| https://github.com/andytrigent/metry360-phase1 | Repository |

## Architecture (actual)

```
Browser
  └─ Vercel static hosting (public/ — plain HTML/CSS/JS, no build step)
       └─ vercel.json rewrites /api/* ──► AWS API Gateway 2g852sgu1i (stage: prod)
            ├─ /api/health          (explicit route)
            └─ /api/{proxy+} ANY    (catch-all, added 2026-07-10)
                 └─ Lambda: sojpe-data-pipeline (python3.11, handler index.lambda_handler)
                      ├─ S3: trigent-c2h-files        (raw files under reports/{report_id}/)
                      ├─ DynamoDB: sojpe-reports      (report metadata, key: report_id)
                      └─ CloudWatch                    (logs + metrics)
```

Region: `ap-south-1`. There is **no Flask server, no SQLite** — earlier docs referencing them are historical.

## How the weekly flow works

1. **Upload** — Akash selects the 7 raw Excel exports on the upload page. The page base64-encodes the actual file contents and POSTs them to `/api/upload`.
2. **Storage** — Lambda writes each file to S3 (`reports/{report_id}/{filename}`) and records real names/sizes in DynamoDB.
3. **Data period detection** — Lambda reads the reporting period from *inside* the files (the `Period: dd/mm/yy To dd/mm/yy` header in the Selects/Renege reports; Joiners From/To dates as fallback) and stores `data_week_ending`. **Week labels always reflect the data, never the upload date.**
4. **Dashboard** — `/api/reporting-period` drives the sidebar week list (all Fridays of the data month, shown as `Ending 29-May`) and the header (`Week Ending 29-May`). Report History renders exclusively from `/api/reports`: data week, upload time, file list, status workflow (DRAFT → IN_REVIEW → APPROVED).

### Week display convention

No week numbers anywhere. Weeks are identified by their **ending Friday** in short form (`Ending 26-Jun`). Months with 5 Fridays are supported.

## API reference

Base: `https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod` (or relative `/api/*` from the Vercel domain)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Service health + infrastructure names |
| `/api/upload` | POST | `{reportId?, files: [{name, fileType, content(base64)}]}` → stores to S3, detects data period, runs pipeline |
| `/api/reports` | GET | All reports, newest first, with file lists and `data_week_ending` |
| `/api/reports/{id}` | GET | Report metadata + S3 file listing |
| `/api/reports/{id}/approve` | POST | `{reviewerName, decision, notes}` → APPROVED |
| `/api/reports/{id}/reprocess` | POST | Re-run pipeline for a report |
| `/api/reporting-period` | GET | Current week/month from latest report's **data period** (`source: data_period` / `uploads` / `current_date`) |

## Deploy procedures

**Frontend** (from repo root): `vercel --prod --yes`

**Backend** — the Lambda handler config is `index.lambda_handler`, so the source file must be zipped as `index.py`:

```bash
cp backend/lambda_handler.py index.py
python -c "import zipfile; z=zipfile.ZipFile('lambda_deploy.zip','w',zipfile.ZIP_DEFLATED); z.write('index.py'); z.close()"
aws lambda update-function-code --function-name sojpe-data-pipeline --zip-file fileb://lambda_deploy.zip --region ap-south-1
```

AWS CLI auth: `aws login` (session-based, expires).

## What is real vs. still sample (honest status)

**Real, verified end-to-end (2026-07-10):**
- Upload → S3 → DynamoDB → Report History, with data-period detection
- Reporting-period API and all week-ending labels
- View switching, director collapse/expand, landing-page API status
- Reprocess and Approve endpoints

**Still hardcoded sample data (Phase 1 remaining work):**
- All dashboard *metric values* (positions, coverage %, every AM row in every view) — the Lambda pipeline counts steps but does not yet parse the Excel files or compute AM-level aggregates
- Week navigation views show placeholders, not per-week data
- Review Details & Audit Trail view is static
- CSV export uses fixed rows
- Some workflow buttons (Mark for Review, Download Files, View Details) are visual only
- Dashboard org-chart tables are hardcoded (a config-driven org chart exists at `public/config/org-chart.json` + admin UI but the tables don't consume it yet)

## Data note (important)

Uploads before 2026-07-10 **never reached AWS** (no gateway route + the page sent only file names + the Lambda was a mock). Any weekly reports from before that date exist only on the uploader's machine and must be re-uploaded. The current seed report `REPORT-3DDF59BC5F60` contains the repo's raw files, which are the **25–29 May 2026** week.

## Repository layout

```
metry360-phase1/
├── public/                  ← everything Vercel serves
│   ├── index.html           ← landing page with API status check
│   ├── dashboard.html       ← the dashboard (all views in one file)
│   ├── upload-new.html      ← 7-file upload with base64 payload
│   ├── config/org-chart.json / org-chart.html
│   └── js/org-chart-manager.js
├── backend/
│   └── lambda_handler.py    ← deployed to Lambda as index.py (see Deploy)
├── vercel.json              ← static hosting + /api/* rewrite to API Gateway
└── *.md                     ← older status docs are historical; this README is current
```

## Reference documents (business logic)

- `../CLAUDE.md` — full business context, metrics formulas, 83-step pipeline spec
- `../Business Requirements Document- QMetry.pdf`
- `../SOJPE_Phase1_Data_Walkthrough_for_Andy_1.pdf` — the manual SOP being automated
- `../Raw reports used for SOJPE/` — sample raw files (data week 25–29 May 2026)
