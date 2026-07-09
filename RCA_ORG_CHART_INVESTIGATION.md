# 🔍 ROOT CAUSE ANALYSIS - Organization Chart Issue

**Date**: July 9, 2026  
**Issue**: Incorrect org chart structure in dashboard  
**Status**: Under Investigation (No code changes yet)

---

## 📋 ISSUE SUMMARY

The dashboard org chart is incorrect. Current hardcoded structure doesn't match actual Trigent organizational hierarchy.

**Reported by**: Akash Devnath (MIS)  
**Evidence**: Email dated Jul 9, 2026, 2:38 PM

---

## ❌ WHAT'S WRONG

### Current (Incorrect) Dashboard Structure
```
Jyothsna (Director) - 5 AMs
  - Priyanka Gadadmathad
  - Tanu Gupta
  - Bharath C N
  - Anuradha H
  - Roshan Dominic

Sanjib (Director) - 5 AMs
  - Bindu T S
  - Abhilash S
  - Kavita Nyamagoud
  - Vivek Singh Sengar  ❌ WRONG
  - Manisha              ❌ WRONG

Total: 10 AMs
```

### Actual (Correct) Structure - Reported by Akash

```
Jyothsna (Director)
  - Priyanka Gadadmathad (AM)
  - Tanu Gupta (AM)
  - Bharath C N (AM)
  - Anuradha H (AM)
  - Roshan Dominic (AM)
  → Total: 5 AMs

Sanjib (Vice President)
  - Abhilash S (AM)
  - Bindu T (SAM)
  - Kavita N (AM)
  → Total: 3 AMs

Praveen (Associate Director)
  - Sankeerth D (AM)
  - Sachin L (AM)
  → Total: 2 AMs

Vivek (Associate Director)
  - [Data needed - not specified in email]
  → Total: ? AMs

Manisha (Independent Span/Lead)
  - Sathish Kumar B (SAM)
  - Nishant Tyagi (AM)
  - Divya Lakshmi (SAM)
  → Total: 3 AMs

Grand Total: 12+ Account Managers across 5 Leads/Directors
```

---

## 🔴 ROOT CAUSE ANALYSIS

### What We Know:
1. ✅ Dashboard has hardcoded sample data
2. ✅ Sample data doesn't match actual org structure
3. ✅ Akash confirmed correct org chart structure
4. ❓ **UNKNOWN**: What's in the actual uploaded raw files (S3)?
5. ❓ **UNKNOWN**: What's in DynamoDB reports table?
6. ❓ **UNKNOWN**: Where does the actual org chart come from?

### Missing Information:

| Question | Current Status | Impact |
|----------|---|---|
| What raw files were uploaded? | ❌ UNKNOWN | Need to check S3 bucket |
| What's the source of org hierarchy? | ❌ UNKNOWN | Ceipal? People.trigent? Config? |
| Is org chart in the 7 Excel files? | ❓ UNKNOWN | Need to review raw file structure |
| What reports are in DynamoDB? | ❌ UNKNOWN | Need to check database |
| Are there multiple org hierarchies? | ❓ UNKNOWN | One per month? One per week? |

---

## 🔎 INVESTIGATION PLAN

### Step 1: Check Data Sources
- [ ] Review S3 bucket (`trigent-c2h-files`) for uploaded files
- [ ] Check DynamoDB table (`sojpe-reports`) for stored reports
- [ ] Identify what raw files were actually uploaded

### Step 2: Understand Org Chart Source
- [ ] Is org chart in Ceipal ATS exports?
- [ ] Is org chart in People.trigent HRMS exports?
- [ ] Is there a separate org chart configuration?
- [ ] How often does org chart change?

### Step 3: Verify Data Structure
- [ ] Do the 7 raw Excel files contain org hierarchy?
- [ ] What columns contain Director/AM relationship?
- [ ] Is there a "Reporting Manager" or "BU Head" field?

### Step 4: Current Data Issue
- [ ] Why is Vivek showing as under Sanjib instead of Associate Dir?
- [ ] Why is Manisha hardcoded under Sanjib instead of independent span?
- [ ] Are there other incorrect relationships?

---

## 📊 CURRENT HARDCODED DATA

**File**: `public/dashboard.html`  
**Lines**: 673-760 (Recruitment Scorecard Table)  
**Issue**: Hardcoded sample data with:
- Wrong org hierarchy
- Wrong director/span assignments
- Missing independent leads (Manisha, Praveen, Vivek)
- Incorrect team relationships

---

## 🎯 WHAT NEEDS TO HAPPEN

### Before Code Changes:
1. ✅ Confirm correct org chart (Done - Akash provided it)
2. ❌ Find where org chart data should come from (S3/DB/Excel?)
3. ❌ Identify if data is available in uploaded raw files
4. ❌ Determine if org chart needs to be pulled dynamically or hardcoded
5. ❌ Check if there's a master org chart reference file

### After RCA Complete:
1. Update dashboard to use correct org chart
2. If data is in Excel files: parse and use it
3. If data is in database: query and use it
4. If data is static: update hardcoded structure
5. Add safeguard: validate org chart against expected structure

---

## 📝 NEXT STEPS

### Immediate Actions Needed:
1. **Access S3 bucket** → List all uploaded files
2. **Check DynamoDB** → View stored reports and metadata
3. **Review raw file structure** → Identify org hierarchy fields
4. **Confirm data availability** → Is org chart in the files or external?

### Decisions Needed:
- [ ] Should org chart be hardcoded or dynamic?
- [ ] What's the authoritative source of truth?
- [ ] How often does org chart update?
- [ ] Should dashboard adapt to real-time org changes?

---

## ⚠️ CRITICAL FINDINGS

### Issue Severity: HIGH
- **Impact**: Incorrect team hierarchy displayed to all users
- **Trust**: Users see wrong reporting relationships
- **Decisions**: Wrong org structure could lead to bad business decisions
- **Compliance**: Potential accuracy issues in reports

### Affected Users:
- Dashboard viewers (Rhoni, Akash, team)
- Report reviewers (Akash)
- All stakeholders relying on dashboard data

---

## 📋 EVIDENCE

### From Akash's Email (Jul 9, 2:38 PM):
- Manisha is NOT under Sanjib
- Manisha has independent span: Sathish, Nishant, Divya
- Sanjib (VP): Abhilash, Bindu, Kavita only (3 AMs)
- Praveen (Assoc Dir): Sankeerth, Sachin (2 AMs)
- Vivek (Assoc Dir): Listed but no AMs mentioned
- Total AMs: 12+ across 5 leads/directors

### Current Dashboard Shows:
- Jyothsna: 5 AMs
- Sanjib: 5 AMs (incorrect - includes Vivek & Manisha)
- Missing: Manisha as independent, Praveen, Vivek as leads
- Total: 10 AMs (should be 12+)

---

## 🔐 DATA RETENTION

### Files That May Contain Org Chart:
1. **Ceipal Exports**:
   - Coverage Raw Report.xlsx
   - Submissions (Avg Subs) Raw Report.xlsx
   - Weekly Selects Report.xlsx
   - Weekly Renege Report.xlsx

2. **People.trigent Exports**:
   - Weekly Joiners Report.xlsx
   - Weekly Exits Report.xlsx
   - Staffing Report for YTJ & YTE.xlsx

3. **Potential Org Chart Fields**:
   - "Director" / "BU Head"
   - "Account Manager" / "Reporting Manager"
   - "Span" / "Portfolio"
   - "Position" / "Role"

---

## 📌 STATUS

**Investigation Status**: 🔴 NOT STARTED  
**RCA Status**: 🔴 IN PROGRESS  
**Code Changes**: 🟢 BLOCKED (waiting for RCA results)

**What's Blocked**:
- No dashboard updates until we understand data source
- No hardcoding of org chart until verified
- No code changes until we know where truth is

---

## 📧 RESPONSE TO ANDY (User's Request)

**Response to "need to review and figure this out"**: ✅ AGREED

**What I'm Doing**:
1. Document all known facts (org chart structure from Akash)
2. Identify missing information (data sources, S3 contents, DB contents)
3. Create investigation plan (where to look, what to check)
4. Hold off on code changes until we have complete picture

**What We Need From Team**:
1. ✅ Correct org chart structure (provided by Akash)
2. ❓ Source of org chart data (where does it come from?)
3. ❓ Upload history (what files were actually uploaded?)
4. ❓ Data validation (org chart in the raw files?)

---

## 🎯 CONCLUSION

**We do NOT have a complete picture yet.**

- ✅ We know what's WRONG (hardcoded structure)
- ✅ We know what's CORRECT (Akash's org chart)
- ❌ We DON'T know where data SHOULD come from
- ❌ We DON'T know if data is in uploaded files or external
- ❌ We DON'T know if this changes weekly/monthly

**Next**: Investigate S3 & DynamoDB to find actual data source, then determine appropriate fix.

---

**Investigation Date**: July 9, 2026  
**Initiated By**: Andy (Development)  
**Requested By**: Akash (MIS)  
**Status**: 🔴 Awaiting Data Access & Investigation

