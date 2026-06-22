# Phase 1 Deployment Checklist

**Project:** SOJPE C2H - Recruiting Operations Intelligence Platform  
**Phase:** 1 (Automation & Dashboard)  
**Status:** READY FOR DEPLOYMENT  
**Date:** June 22, 2026

---

## ✅ PRE-DEPLOYMENT (Complete)

### Development
- [x] Dashboard UI complete (5 views, Figma compliant)
- [x] Upload/Admin panel complete
- [x] Flask backend API complete
- [x] Data pipeline fully implemented (83 steps)
- [x] Database schema designed
- [x] All endpoints tested
- [x] Error handling implemented
- [x] Logging configured

### Quality Assurance
- [x] Code reviewed
- [x] Unit tests on pipeline logic
- [x] End-to-end workflow tested
- [x] File upload tested (7 files)
- [x] Report generation tested
- [x] Metrics verification complete
- [x] RAG status indicators verified
- [x] Dashboard rendering tested (all 5 views)

### Documentation
- [x] README.md (complete)
- [x] PHASE1_COMPLETE.md (detailed delivery)
- [x] DEPLOYMENT_CHECKLIST.md (this file)
- [x] API documentation
- [x] Data pipeline documentation
- [x] Installation instructions

### Configuration
- [x] requirements.txt prepared
- [x] Launcher script (run.ps1) tested
- [x] Database initialization script ready
- [x] Port configuration finalized (8000, 5000)
- [x] Logging configuration complete

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Environment Setup
**Time Required:** 5 minutes  
**Owner:** DevOps / IT

- [ ] Install Python 3.8 or higher
  ```powershell
  # Verify installation
  python --version
  ```

- [ ] Clone/copy project to production server
  ```powershell
  # Copy entire metry360-phase1 folder
  Copy-Item -Path D:\experiments\gcc-qmetry\metry360-phase1 -Destination "C:\Program Files\SOJPE" -Recurse
  ```

- [ ] Verify all required files exist
  - [ ] dashboard.html
  - [ ] upload.html
  - [ ] app.py
  - [ ] requirements.txt
  - [ ] run.ps1
  - [ ] index.html

### Step 2: Dependency Installation
**Time Required:** 3 minutes  
**Owner:** DevOps / IT

```powershell
cd "C:\Program Files\SOJPE\metry360-phase1"
pip install -r requirements.txt --upgrade
```

- [ ] Verify all packages installed
  ```powershell
  pip list | findstr Flask,pandas,openpyxl
  ```

### Step 3: Port Availability Check
**Time Required:** 2 minutes  
**Owner:** Network / IT

```powershell
# Verify ports 8000 and 5000 are available
netstat -ano | findstr :8000
netstat -ano | findstr :5000
```

- [ ] Port 8000 is available (HTTP server)
- [ ] Port 5000 is available (Flask API)
- [ ] Firewall allows inbound connections
- [ ] Update firewall rules if needed

### Step 4: Database Initialization
**Time Required:** 1 minute  
**Owner:** DevOps / IT

```powershell
# Flask will auto-create database on first run
# No manual action needed - verified during startup
```

- [ ] reports.db will be created on first startup
- [ ] Backup strategy planned (see below)

### Step 5: Service Startup
**Time Required:** 2 minutes  
**Owner:** DevOps / IT

```powershell
# Option A: Automated (Recommended)
.\run.ps1

# Option B: Manual
# Terminal 1:
python -m http.server 8000

# Terminal 2:
python app.py
```

- [ ] HTTP server started (Port 8000)
- [ ] Flask API started (Port 5000)
- [ ] No error messages in console
- [ ] Both services responding

### Step 6: Connectivity Verification
**Time Required:** 2 minutes  
**Owner:** QA / IT

```powershell
# Test all access points
Start-Process "http://localhost:8000"
Start-Process "http://localhost:8000/dashboard.html"
Start-Process "http://localhost:8000/upload.html"

# Test API
curl http://localhost:5000/api/health
```

- [ ] Welcome page loads (http://localhost:8000)
- [ ] Dashboard loads with sample data
- [ ] Upload page loads and shows file picker
- [ ] API responds to health check
- [ ] No browser console errors

### Step 7: First Report Test
**Time Required:** 5 minutes  
**Owner:** QA / Business Analyst

```
1. Go to http://localhost:8000/upload.html
2. Create or use sample 7 Excel files
3. Upload files via drag-drop or click
4. Click "Process Files & Generate Report"
5. Wait for processing (~60 seconds)
6. Verify report appears with correct data
7. Go to dashboard and verify display
8. Approve report and verify status change
```

- [ ] Sample files uploaded successfully
- [ ] Processing completes without errors
- [ ] Report generated with correct report ID
- [ ] Report appears in history list
- [ ] Dashboard displays correct metrics
- [ ] RAG indicators show correct colors
- [ ] Can approve/publish report
- [ ] Approved report becomes "MASTER"

### Step 8: Data Backup Configuration
**Time Required:** 10 minutes  
**Owner:** IT / DevOps

```powershell
# Create backup script
New-Item -ItemType Directory -Path "C:\Backups\SOJPE"

# Backup database daily
# (Add to Windows Task Scheduler or cron)
Copy-Item -Path "C:\Program Files\SOJPE\metry360-phase1\reports.db" `
          -Destination "C:\Backups\SOJPE\reports_$(Get-Date -Format 'yyyyMMdd').db"
```

- [ ] Backup folder created
- [ ] Backup script tested
- [ ] Automated backup scheduled (daily at 2 AM)
- [ ] Retention policy set (keep last 30 days)
- [ ] Restore procedure documented

---

## 🔐 POST-DEPLOYMENT

### Monitoring Setup
- [ ] Set up log monitoring (check app.py console output)
- [ ] Configure alerts for:
  - [ ] Service crashes
  - [ ] Port connection errors
  - [ ] Database access failures
  - [ ] Processing errors
- [ ] Establish response procedure for alerts

### Access Control
- [ ] Document access points:
  - [ ] Dashboard: http://[server]:8000/dashboard.html
  - [ ] Upload: http://[server]:8000/upload.html
  - [ ] API: http://[server]:5000
- [ ] Communicate URLs to users
- [ ] Set up bookmark/favorites
- [ ] Document usernames/passwords (if any)

### Performance Tuning
- [ ] Monitor first week of usage
- [ ] Check report generation time (should be ~60 sec)
- [ ] Monitor database file size growth
- [ ] Check server CPU/memory usage
- [ ] Adjust if needed

### User Training
- [ ] Schedule training session with operators
- [ ] Document weekly workflow
- [ ] Provide quick reference guide
- [ ] Test with actual 7-file upload
- [ ] Verify all 5 dashboard views work
- [ ] Practice approve/publish workflow

---

## 📋 WEEKLY OPERATIONS

### Monday 8:00 AM Routine

```
1. [Ceipal] Download 7 raw Excel files
2. [Dashboard] Go to upload.html
3. [Upload] Drag files into upload area
4. [Process] Click "Process Files"
5. [Wait] Wait ~60 seconds for processing
6. [Review] Go to dashboard.html
7. [Verify] Check all metrics look correct
8. [Alert] Review alert panel (green/amber/red)
9. [Approve] Click "Approve & Publish" if correct
10. [Share] Share dashboard URL with team
11. [Archive] Note the report ID for archive
```

**Expected Time:** 10-15 minutes

### Key Success Indicators
- [ ] Report generated by 8:30 AM
- [ ] All 7 input files processed
- [ ] Metrics updated from previous week
- [ ] Coverage % between 50-100%
- [ ] Avg Sub between 2-5
- [ ] Team names match expectations
- [ ] No error messages in console
- [ ] Report published and visible

### Troubleshooting During Operations
- [ ] If upload fails: Check file format is .xlsx
- [ ] If processing stalls: Check console for errors
- [ ] If metrics look wrong: Verify input files are correct
- [ ] If page freezes: Refresh browser (F5)
- [ ] If API offline: Restart Flask (python app.py)

---

## 🔄 MAINTENANCE SCHEDULE

### Daily (Automated)
- [ ] Backup database (2 AM)
- [ ] Check service is running
- [ ] Monitor log files for errors

### Weekly (Manual)
- [ ] Review report metrics for anomalies
- [ ] Verify all 7 input files are received
- [ ] Check that approved reports are current
- [ ] Spot-check dashboard calculations

### Monthly (Scheduled)
- [ ] Database maintenance check
- [ ] Backup retention review
- [ ] User access audit
- [ ] Performance metrics review
- [ ] Update documentation if needed

### Quarterly (Planning)
- [ ] Plan Phase 2 enhancements
- [ ] Review user feedback
- [ ] Assess resource needs
- [ ] Security audit
- [ ] Cost analysis

---

## 🚨 EMERGENCY PROCEDURES

### Service Crash or Unexpected Shutdown

**Diagnosis:**
```powershell
# Check if services are running
Get-Process python
Get-Process python | Where-Object {$_.CommandLine -like "*http.server*"}
Get-Process python | Where-Object {$_.CommandLine -like "*app.py*"}
```

**Recovery:**
```powershell
# Kill existing processes if needed
Stop-Process -Name python -Force

# Restart services
cd "C:\Program Files\SOJPE\metry360-phase1"
.\run.ps1
```

- [ ] Both services restarted
- [ ] No error messages
- [ ] Dashboard loads
- [ ] API responds

### Database Corruption

**Backup Recovery:**
```powershell
# If reports.db is corrupted
1. Stop Flask (Ctrl+C)
2. Copy backup to reports.db.bak
3. Delete reports.db
4. Restart Flask (creates fresh database)
5. Restore data from last backup
```

- [ ] Database recovered from backup
- [ ] Recent reports intact
- [ ] Notify manager of data loss period

### Port Conflict

**Resolution:**
```powershell
# Find what's using port 8000 or 5000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID [PID] /F

# Or change ports in app.py and restart
```

- [ ] Port freed
- [ ] Service restarted
- [ ] Dashboard accessible

---

## ✅ SIGN-OFF CHECKLIST

### Development Team
- [ ] Code reviewed and approved
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Known issues documented

**Signed:** ___________________  
**Date:** _________________

### QA Team
- [ ] Test plan executed
- [ ] No critical bugs found
- [ ] Performance acceptable
- [ ] Security review complete

**Signed:** ___________________  
**Date:** _________________

### Operations/DevOps
- [ ] Environment prepared
- [ ] Deployment tested
- [ ] Monitoring configured
- [ ] Backup plan in place

**Signed:** ___________________  
**Date:** _________________

### Business/Management
- [ ] Requirements met
- [ ] Ready for production
- [ ] User training scheduled
- [ ] Go-live approved

**Signed:** ___________________  
**Date:** _________________

---

## 📞 SUPPORT CONTACTS

| Role | Name | Email | Phone |
|------|------|-------|-------|
| Project Owner | Rhoni Thomas | rhoni_t@trigent.com | — |
| Dev Contact | Andy | — | — |
| IT Support | — | — | — |
| Business Analyst | — | — | — |

---

## 📝 NOTES

```
Deployment Notes:
(Add deployment observations and issues here)




Post-Deployment Notes:
(Add any issues discovered after deployment)




Phase 2 Planning Notes:
(Add enhancement requests and feedback)


```

---

**Deployment Status:** ✅ **READY**  
**Last Updated:** June 22, 2026  
**Next Review:** [After first production run]
