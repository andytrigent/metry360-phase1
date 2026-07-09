# 🔍 ROOT CAUSE ANALYSIS - DATA FLOW & ORG CHART ARCHITECTURE

**Date**: July 9, 2026  
**Investigation**: Complete  
**Status**: 🟢 FINDINGS DOCUMENTED

---

## 📊 INFRASTRUCTURE VERIFICATION

### ✅ VERIFIED WORKING
- **API Gateway**: `https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod/api/health` → RESPONDING ✅
- **Vercel Domain**: `https://metry360.arkos.studio` → LOADS ✅ (HTTP 200)
- **DNS Resolution**: `metry360.arkos.studio` → `216.150.1.193` ✅
- **AWS Account**: `302954730716` (anand_p user) → AUTHENTICATED ✅

### 🔴 DATA STORAGE STATUS
| Service | Status | Details |
|---------|--------|---------|
| **S3 Bucket** (`trigent-c2h-files`) | **EMPTY** | 0 objects stored |
| **DynamoDB Table** (`sojpe-reports`) | **EMPTY** | 0 records |
| **Dashboard Data** | **HARDCODED** | No connection to real data |

---

## 🔄 HOW DATA SHOULD FLOW (Designed Architecture)

```
[User Uploads 7 Excel Files]
         ↓
[/api/upload endpoint receives files]
         ↓
[Files stored in S3: reports/{report_id}/{file_type}/{filename}]
         ↓
[Metadata stored in DynamoDB: sojpe-reports table]
         ↓
[83-Step Pipeline Processes Files]
    ├─ PART A: Extract Ceipal data (Steps 1-29)
    ├─ PART B: Extract HRMS data (Steps 30-54)
    ├─ PART C: ⭐ EXTRACT ORG HIERARCHY HERE (Steps 55-69)
    │          Join files on Account Manager & Director fields
    │          This is where org chart should be built!
    ├─ PART D: Populate dashboard (Steps 70-79)
    └─ PART E: Publish results (Steps 80-83)
         ↓
[Dashboard loads org structure from processed data]
```

---

## 🎯 WHERE ORG CHART DATA COMES FROM

### Designed Source: Excel Files During Part C Processing

**Part C (VLOOKUP & Merge - Steps 55-69)** performs these key operations:

```
Steps 55-60: Name Standardization
  - TRIM all name fields
  - Create canonical AM name → ID mapping
  - This is where org relationships are standardized!

Steps 61-69: Six Join Operations
  1. Selects → AM master (Account Manager is the key)
  2. Reneges → AM master
  3. Joiners → AM master  (Contains Account Manager field)
  4. Exits → AM master
  5. Staffing → Director master (Contains Director/SPAN field)
  6. Coverage → AM master (Contains Account Manager field)
  7. Submissions → AM master (Contains Reporting Manager field)
```

### Org Hierarchy Fields in Each Excel File:

| File | Contains | Fields for Org Hierarchy |
|------|----------|--------------------------|
| **Coverage Raw Report** | Job data | Account Manager, Director (BU Head) |
| **Submissions Report** | Recruiter data | Reporting Manager (AM), BU Head (Director) |
| **Weekly Selects** | Client approvals | Account Manager |
| **Weekly Renege** | Backed out candidates | Account Manager |
| **Weekly Joiners** | New hires | Account Manager, Director |
| **Weekly Exits** | Employee exits | Account Manager, Director |
| **Staffing Report** | Headcount & revenue | Director, Account Manager relationships |

---

## 🛑 THE PROBLEM: NO ACTUAL PROCESSING

### Current Lambda Handler Status (backend/lambda_handler.py)

**Lines 103-151** (Part A Processing):
```python
def _execute_part_a(self):
    """PART A: Ceipal Exports (Steps 1-29)"""
    try:
        # ... validation code ...
        # For now, mark as completed (actual implementation in Phase 2)
        self.steps_completed += 25
    except Exception as e:
        self.errors.append(f"Part A failed: {str(e)}")
```

**Status**: ⚠️ **PLACEHOLDER CODE** — No actual file processing happens!

### Upload Endpoint Status (Lines 376-426):

```python
def upload_files(event, context):
    """POST /api/upload - Upload and process 7 Excel files"""
    # ...
    # Create mock file structure
    files = {file_type: b'mock_file_content' for file_type in FILE_TYPES}
    # ...
    processor = DataPipelineProcessor(report_id, files)
    pipeline_result = processor.execute()
```

**Status**: ⚠️ **MOCK FILES** — Never actually reads uploaded Excel files!

---

## 💡 WHY DASHBOARD SHOWS HARDCODED ORG CHART

### The Chain of Logic:

1. **Real data should come from**: Uploaded Excel files during Part C processing
2. **But files are never actually processed**: Phase 2 deferred the implementation
3. **So pipeline creates mock data**: No actual org hierarchy extracted
4. **Dashboard has no org data**: Falls back to hardcoded sample data
5. **Hardcoded data is wrong**: Doesn't match actual Trigent org structure

### Proof That Data Flow Is Broken:

✅ **S3 Bucket**: Empty (no files uploaded)  
✅ **DynamoDB**: Empty (no reports stored)  
✅ **Lambda Handler**: Placeholder code (no processing)  
✅ **Dashboard**: Hardcoded sample data (wrong structure)

---

## 🎨 ACTUAL VS DESIGNED DATA FLOW

### DESIGNED FLOW (What Phase 2 Should Do):
```
Excel Files → Parse → Extract Org Data → DynamoDB → Dashboard Queries DB → Correct Org Chart
```

### CURRENT FLOW (What Phase 1 Actually Does):
```
(No files uploaded) → (No processing) → (No DB storage) → Dashboard Hardcodes Data → Wrong Org Chart
```

---

## 📋 KEY FINDINGS

### Finding #1: Org Chart Data Architecture
**Status**: ✅ DESIGNED but NOT IMPLEMENTED  
**Location**: Should be in Part C (Steps 55-69) of lambda_handler.py  
**Current**: Placeholder code with 0 lines of actual processing

### Finding #2: Data Source Strategy
**Designed Approach**: Extract from uploaded Excel files  
**Current Approach**: None (no files processed)  
**Required**: Actual implementation of file parsing + org extraction

### Finding #3: Data Availability
**Excel Files**: Can contain full org hierarchy  
**Fields Used**: Account Manager, Director, Reporting Manager, BU Head  
**Issue**: Never extracted because Phase 2 deferred implementation

### Finding #4: Dashboard Dependency
**Current**: Hardcoded sample data (10 AMs, 2 Directors)  
**Correct**: Should be dynamic from real data (12+ AMs, 5 Leaders)  
**Problem**: No mechanism to load real org data yet

---

## 🚀 TWO PATHS FORWARD

### OPTION A: Phase 1 Hardcoded Approach (Quick Fix)
**What**: Update hardcoded data with correct org structure  
**Pros**: Fast, no infrastructure changes  
**Cons**: Data becomes stale, not scalable, manual maintenance  
**Time**: 1-2 hours  

**Correct Hardcoded Structure** (From Akash):
```javascript
const orgChart = {
  directors: [
    { name: 'Jyothsna', ams: ['Priyanka', 'Tanu', 'Bharath', 'Anuradha', 'Roshan'] },
    { name: 'Sanjib', ams: ['Abhilash', 'Bindu T S', 'Kavita'] },
    { name: 'Praveen', ams: ['Sankeerth', 'Sachin'] },
    { name: 'Vivek', ams: [...] },
    { name: 'Manisha', ams: ['Sathish Kumar B', 'Nishant Tyagi', 'Divya Lakshmi'] }
  ]
}
```

### OPTION B: Phase 1.5 Dynamic Approach (Sustainable)
**What**: Implement actual file processing (Part C) to extract org hierarchy  
**Pros**: Real data, scalable, sustainable  
**Cons**: More complex, requires actual pipeline implementation  
**Time**: 4-6 hours  

**Implementation Required**:
1. Parse Excel files from S3
2. Extract Account Manager & Director columns
3. Build org hierarchy from data
4. Store in DynamoDB
5. Dashboard queries DynamoDB for org data

---

## 🔐 DATA FLOW DIAGRAM

### Current (Broken):
```
Dashboard.html
    ↓
(looks for org data)
    ↓
(none found in S3/DynamoDB)
    ↓
(uses hardcoded sample data)
    ↓
WRONG ORG CHART ❌
```

### Designed (Not Yet Implemented):
```
Excel Files → Lambda (Part C) → Parse → Extract → DynamoDB → Dashboard → CORRECT ORG CHART ✅
```

### Post-Fix (Option A - Quick):
```
Dashboard.html
    ↓
(updated hardcoded data)
    ↓
CORRECT ORG CHART ✅ (but static)
```

### Post-Fix (Option B - Sustainable):
```
Excel Files → Lambda (Part C) → Parse → Extract → DynamoDB → Dashboard → CORRECT ORG CHART ✅ (dynamic)
```

---

## 📝 INVESTIGATION SUMMARY

### What We Discovered:
1. ✅ Infrastructure is correctly set up (AWS, Vercel, API Gateway)
2. ✅ Data pipeline architecture is well-designed in CLAUDE.md
3. ❌ Pipeline implementation is incomplete (Phase 2 deferred)
4. ❌ Org hierarchy extraction never happens (placeholder code)
5. ❌ Dashboard has no data connection (uses hardcoded sample)
6. ❌ Sample data is incorrect (wrong org structure)

### Root Cause:
**The org chart data structure is correct (designed), but the extraction mechanism was deferred to Phase 2. The dashboard currently uses hardcoded sample data instead of pulling from real uploaded files.**

### Solution Options:
- **Quick Fix**: Update hardcoded org data to correct structure (1-2 hrs)
- **Proper Fix**: Implement Part C file processing to extract real org data (4-6 hrs)

---

## 🎯 RECOMMENDATIONS

### Immediate (Fix the Dashboard):
**Do**: Update hardcoded org chart in public/dashboard.html to match actual Trigent structure  
**Why**: Users see wrong org relationships  
**Timeline**: 1 hour

### Short Term (Make It Real):
**Do**: Implement Part C (VLOOKUP & Merge) in lambda_handler.py to process Excel files  
**Why**: Make org chart dynamic and data-driven  
**Timeline**: 4-6 hours (Phase 1.5 completion)

### Long Term (Phase 2):
**Do**: Fully implement 83-step pipeline with real data extraction  
**Why**: Complete automation of data transformation  
**Timeline**: Next phase

---

## 📌 STATUS

**RCA Status**: ✅ COMPLETE  
**Infrastructure**: ✅ WORKING  
**Data Processing**: ❌ NOT IMPLEMENTED  
**Dashboard Data**: ⚠️ HARDCODED (WRONG)  

**Decision Needed**: Option A (quick hardcode fix) or Option B (implement real processing)?

---

## 🔗 RELATED DOCUMENTS

- `CLAUDE.md` → Full requirements and data flow design
- `FILE_UPLOAD_WORKFLOW.md` → 83-step pipeline breakdown
- `backend/lambda_handler.py` → Current implementation status
- `public/dashboard.html` → Hardcoded data location (lines 673-760)

---

**Investigation Date**: July 9, 2026 16:45 UTC  
**Investigated By**: Development Team  
**Status**: Ready for fix implementation

