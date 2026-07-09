# 📧 RCA RESPONSE EMAIL DRAFT

**To**: Andy, Akash, Rhoni  
**Subject**: Organization Chart Issue - RCA Investigation Required (No Code Changes Yet)

---

## Email Body

Hi Andy & Akash,

Thank you for identifying the organizational chart discrepancy. You're absolutely right — we need to complete a proper RCA before making any code changes.

**Confirmed Issue**: The dashboard's hardcoded organization structure doesn't match Trigent's actual hierarchy.

---

## ✅ WHAT WE KNOW (Confirmed)

Based on Akash's detailed feedback, the correct organizational structure is:

```
Jyothsna (Director)
  ├─ Priyanka Gadadmathad (AM)
  ├─ Tanu Gupta (AM)
  ├─ Bharath C N (AM)
  ├─ Anuradha H (AM)
  └─ Roshan Dominic (AM)
  [5 AMs]

Sanjib (Vice President)
  ├─ Abhilash S (AM)
  ├─ Bindu T (SAM)
  └─ Kavita N (AM)
  [3 AMs]

Praveen (Associate Director)
  ├─ Sankeerth D (AM)
  └─ Sachin L (AM)
  [2 AMs]

Vivek (Associate Director)
  └─ [Details needed]

Manisha (Independent Span/Lead)
  ├─ Sathish Kumar B (SAM)
  ├─ Nishant Tyagi (AM)
  └─ Divya Lakshmi (SAM)
  [3 AMs]

Total: 12+ Account Managers across 5 Leads/Directors
```

---

## ❌ WHAT WE DON'T KNOW YET

Before updating the dashboard, we need to investigate:

1. **Data Source**: Where does the org chart originate?
   - Is it in the Ceipal ATS exports?
   - Is it in the People.trigent HRMS exports?
   - Is there a separate master org chart file?

2. **Uploaded Files**: What was actually uploaded to S3?
   - What raw files are stored in the S3 bucket?
   - Do the Excel files contain org hierarchy data?
   - What fields define the reporting relationships?

3. **Database State**: What's in DynamoDB?
   - What reports have been stored?
   - Does report metadata include org structure?
   - Is there historical org chart data?

4. **Data Structure**: How is hierarchy defined in raw files?
   - Which Excel columns contain Director/AM relationships?
   - Is there a "Reporting Manager" or "BU Head" field?
   - How should we parse org relationships from the files?

---

## 🔎 INVESTIGATION PLAN

### Phase 1: Data Access (Immediate)
- [ ] List S3 bucket (`trigent-c2h-files`) for uploaded files
- [ ] Check DynamoDB table (`sojpe-reports`) for stored data
- [ ] Identify what data is currently available in the system

### Phase 2: Data Analysis
- [ ] Review structure of uploaded Excel files
- [ ] Identify org hierarchy fields in raw exports
- [ ] Map data columns to org chart structure

### Phase 3: Truth Determination
- [ ] Confirm authoritative data source
- [ ] Verify org hierarchy field mappings
- [ ] Validate against Akash's confirmed structure

### Phase 4: Implementation Planning
- [ ] Decide: hardcoded or dynamic org chart?
- [ ] Determine: how often does org chart change?
- [ ] Plan: how to source org data automatically?

---

## 🛑 WHY NO CODE CHANGES YET

**Critical reason**: The current dashboard has hardcoded sample data, not actual production data.

Before we update the org chart, we need to know:
1. **Should it be hardcoded?** (if org never changes)
2. **Should it be dynamic?** (if it changes monthly/weekly)
3. **Where's the data?** (raw files, database, or external config?)

If we hardcode the wrong structure again, we'll just create the same problem.

---

## 📊 WHAT WILL HAPPEN AFTER RCA

Once we've investigated:

### Option A: Org Chart in Raw Files
If the Excel exports contain org hierarchy:
- Extract org structure from the 7 raw files
- Automatically build org chart from actual data
- Dashboard will be accurate for each week's data

### Option B: Org Chart in Database
If org hierarchy is stored after processing:
- Query DynamoDB for current org structure
- Display live org hierarchy
- Updates automatically as data changes

### Option C: Master Reference File
If org chart is maintained separately:
- Load from master config/file
- Update manually as needed
- Single source of truth for organization

### Option D: External Service
If org comes from People.trigent API:
- Query API directly
- Always current
- Real-time hierarchy

---

## ⏰ TIMELINE

**Today (July 9)**:
- ✅ RCA Investigation initiated
- ✅ Investigation plan created
- ❌ Awaiting data access (S3, DynamoDB)

**Tomorrow (July 10)**:
- [ ] Access S3 & DynamoDB
- [ ] Identify data structure
- [ ] Analyze org hierarchy fields

**This Week**:
- [ ] Complete root cause analysis
- [ ] Determine implementation approach
- [ ] Update dashboard with correct org chart

---

## 🔐 IMPORTANT NOTES

1. **No guessing**: We won't hardcode the org chart again until we know where the truth is
2. **Data-driven**: Organization structure should come from actual data, not assumptions
3. **Sustainability**: Solution should work for any future org changes
4. **Validation**: We'll verify against Akash's confirmed structure before deploying

---

## 📋 REQUIRED FROM TEAM

**From Akash**:
- ✅ Confirmed correct org structure (provided)
- ❓ Any additional org chart details?
- ❓ Is org chart stable or changes frequently?

**From Rhoni/Data**:
- ❓ Do we have access to raw file uploads?
- ❓ Are files stored in S3?
- ❓ Can we access DynamoDB?

---

## ✅ NEXT STEP

**My recommendation**: 
Let me investigate S3 and DynamoDB to understand what data we have, then propose the best approach for sourcing org chart data accurately and sustainably.

---

**Summary**: We have the CORRECT org chart from Akash, but we need to understand WHERE that data should come from in our system before updating the dashboard code.

No changes until we have the complete picture.

Best regards,  
**Andy**

---

**Status**: 🔴 RCA In Progress — No Code Changes Until Complete

