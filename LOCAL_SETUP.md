# Local Setup Guide - SOJPE C2H Phase 1

**Purpose**: Recreate the complete development environment locally from GitHub  
**Time Estimate**: 20-30 minutes  
**Difficulty**: Intermediate

---

## 📋 Prerequisites

### Required Software
- Git (v2.30+)
- Python 3.11+
- Node.js 20+ (for Vercel CLI)
- PowerShell 5.1+ (Windows) or Bash (macOS/Linux)
- pip (Python package manager)

### Required Accounts
- GitHub account (for cloning repository)
- AWS account (for Lambda/API Gateway access) - Optional for local testing
- Vercel account (for front-end deployment) - Optional for local testing

### System Requirements
- RAM: 8GB minimum
- Disk Space: 2GB free
- Internet Connection: Required

---

## 🔧 Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/andytrigent/metry360-phase1.git
cd metry360-phase1

# Verify clone was successful
git status
# Output: On branch main, nothing to commit, working tree clean
```

**What you get:**
```
metry360-phase1/
├── public/                    # Frontend HTML/CSS/JS
│   ├── dashboard.html        # Main dashboard (5 views)
│   ├── upload.html           # File upload interface
│   └── index.html            # Landing page
├── backend/                   # Python backend
│   ├── app.py               # Flask application
│   ├── lambda_handler.py    # AWS Lambda handler
│   └── requirements.txt      # Python dependencies
├── openapi.yaml             # API documentation
├── SOJPE_C2H_API.postman_collection.json  # Postman collection
├── README.md                # Main documentation
├── QUICK_START.md           # Quick reference
└── [other docs and config]
```

---

## 🎯 Step 2: Frontend Setup (Local Testing)

### Option A: Simple HTTP Server (Recommended for Testing)

```bash
# Navigate to project root
cd metry360-phase1

# Start Python HTTP server
python -m http.server 8000

# Output:
# Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**Open in browser:**
```
http://localhost:8000/public/index.html
```

**Alternative ports:**
```bash
# Use port 3000
python -m http.server 3000

# Or with Node.js (if available)
npx http-server public/ -p 3000
```

### Option B: Production Build (Using Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to personal development environment
vercel --dev

# Output will show local URL
# Example: http://localhost:3000
```

---

## 🐍 Step 3: Backend Setup (Local API)

### Install Python Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On macOS/Linux bash:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Dependencies installed:**
- Flask (web framework)
- boto3 (AWS SDK)
- pandas (data processing)
- openpyxl (Excel handling)
- aws-lambda-powertools (logging)

### Run Flask Development Server

```bash
# From backend/ directory
python app.py

# Output:
# * Running on http://127.0.0.1:5000
# * Press CTRL+C to quit
```

**Access API endpoints:**
```bash
# Health check
curl http://localhost:5000/api/health
```

---

## 🌐 Step 4: Configure Environment Variables

Create `.env` file in project root:

```bash
# Backend API Configuration
API_HOST=http://localhost:5000
API_BASE_URL=http://localhost:5000/api

# AWS Configuration (for Lambda testing)
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Vercel Configuration (optional)
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=trigent-ark-os
VERCEL_PROJECT_ID=prj_tmE2PJdRfipzSy11DYDYk5taNbQZ
```

**Security Note**: Never commit .env to Git
- Add to `.gitignore` (already done)
- Use environment variable files for local development only

---

## ✅ Step 5: Verify Local Setup

### Test Frontend
```bash
# Open browser
http://localhost:8000/public/dashboard.html

# Verify:
- ✅ Page loads
- ✅ 5 views visible in sidebar
- ✅ Dashboard displays with sample data
- ✅ No console errors (F12 → Console)
```

### Test Backend API
```bash
# Terminal 1: Start Flask
cd backend
python app.py

# Terminal 2: Test endpoints
# Health check
curl http://localhost:5000/api/health

# Should return:
# {"status":"healthy","service":"sojpe-c2h-api","version":"1.0.0-lambda"}
```

### Test API Documentation

**Swagger UI (if implemented):**
```
http://localhost:5000/api/docs
```

**OpenAPI Specification:**
```
http://localhost:5000/api/openapi.json
```

---

## 📚 Step 6: Using API Documentation

### View OpenAPI/Swagger Specification
```bash
# The specification is in the repository
cat openapi.yaml

# Or view the YAML file in your editor
# Visual Studio Code → Extensions → YAML
```

**OpenAPI Features:**
- Complete endpoint documentation
- Request/response schemas
- Example payloads
- Error codes and descriptions
- Authentication requirements (Phase 2)

### Using Postman Collection

**Import into Postman:**
1. Open Postman application
2. Click "Import" (top left)
3. Select "Upload Files"
4. Choose: `SOJPE_C2H_API.postman_collection.json`
5. Collection imports with all endpoints pre-configured

**Configure Variables:**
- Click "Edit" on collection
- Set `base_url`:
  - Development: `http://localhost:5000`
  - Production: `https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod`

**Test API Endpoints:**
1. Click "Health Check" request
2. Click "Send" button
3. View response in bottom panel
4. Repeat for each endpoint

---

## 🗄️ Step 7: Database Setup

### Local Storage Options

**Option A: SQLite (Simple, File-Based)**
```bash
# Automatically created on first run
# Location: ./reports.db

# To inspect database
python
>>> import sqlite3
>>> conn = sqlite3.connect('reports.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT * FROM reports;")
```

**Option B: AWS DynamoDB (Production)**
```bash
# Requires AWS credentials configured
# See environment variables section above

# Test connection
python
>>> import boto3
>>> dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
>>> table = dynamodb.Table('sojpe-reports')
>>> response = table.scan(Limit=1)
>>> print(response)
```

---

## 🚀 Step 8: File Upload Testing

### Create Test Files Directory
```bash
# Create uploads directory
mkdir uploads

# Copy sample Excel files into this directory
# (or create minimal test files for testing)
```

### Test File Upload Flow
```bash
# Using curl to test upload
curl -X POST http://localhost:5000/api/upload \
  -F "files=@path/to/file1.xlsx" \
  -F "files=@path/to/file2.xlsx"
```

---

## 🔄 Step 9: Git Workflow for Local Development

### Create Feature Branch
```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push origin feature/my-feature

# Create Pull Request on GitHub
```

### Sync with Remote
```bash
# Fetch latest from remote
git fetch origin

# See what's new
git log main..origin/main

# Merge remote changes
git merge origin/main

# Or rebase (cleaner history)
git rebase origin/main
```

---

## 📊 Step 10: Running End-to-End Tests

### Complete Workflow Test
```bash
# Terminal 1: Start Flask backend
cd backend
python app.py

# Terminal 2: Start HTTP server for frontend
cd public
python -m http.server 8000

# Terminal 3: Run tests
cd ..
python -m pytest tests/  # If test suite exists
```

### Manual Integration Test
1. Open http://localhost:8000/public/dashboard.html
2. Verify dashboard loads
3. Click through all 5 views
4. Check browser console for errors
5. Verify API calls are working (Network tab in F12)
6. Test report history
7. Test review details

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -i :8000

# Kill process
# Windows:
taskkill /PID <process_id> /F

# macOS/Linux:
kill -9 <process_id>
```

### Python Version Mismatch
```bash
# Verify Python version
python --version
# Should be 3.11 or higher

# If using multiple Python versions
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Module Not Found Error
```bash
# Ensure virtual environment is activated
which python  # macOS/Linux
where python  # Windows

# If not activated:
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CORS Issues
```bash
# If frontend and backend on different ports
# The backend (Flask) should have CORS enabled

# Check backend logs for CORS errors
# Look for: "Cross-Origin Request Blocked"

# Solution: CORS is configured in app.py
# Verify it's enabled in the Flask app
```

### Git Clone Fails
```bash
# Verify GitHub access
ssh -T git@github.com

# If SSH fails, use HTTPS
git clone https://github.com/andytrigent/metry360-phase1.git

# Configure credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 📖 Documentation Files in Repository

| File | Purpose |
|------|---------|
| README.md | Main overview and quick start |
| QUICK_START.md | Quick reference guide |
| LOCAL_SETUP.md | This file - local development setup |
| DEPLOYMENT_FINAL.md | Production deployment details |
| AWS_LAMBDA_DEPLOYMENT.md | AWS infrastructure setup |
| openapi.yaml | API specification (Swagger/OpenAPI 3.0) |
| SOJPE_C2H_API.postman_collection.json | Postman API collection |
| EMAIL_TO_TEAM.md | Team notification email template |

---

## 🎯 Common Tasks

### View API Documentation
```bash
# Open OpenAPI spec
cat openapi.yaml

# Recommended: Use a tool like Swagger Editor
# Visit: https://editor.swagger.io
# Paste contents of openapi.yaml
```

### Run API Tests
```bash
# Using Postman collection
# 1. Import SOJPE_C2H_API.postman_collection.json into Postman
# 2. Set base_url variable to http://localhost:5000
# 3. Run each request in the collection

# Or using curl:
curl http://localhost:5000/api/health
curl http://localhost:5000/api/reports
```

### Deploy Frontend Locally
```bash
# Option 1: HTTP Server
cd public
python -m http.server 8000

# Option 2: Vercel Local
vercel dev

# Option 3: Node HTTP Server
npx http-server public/
```

### Deploy to Production
```bash
# Push to main branch
git push origin feature/branch main

# Automatic deployment via GitHub Actions to Vercel
# (if configured)

# Or manual Vercel deployment
vercel --prod --yes --scope trigent-ark-os
```

---

## 📝 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600"
        }
      ]
    }
  ]
}
```

### .vercelignore
```
backend/
*.py
requirements.txt
.env
```

### .gitignore
```
venv/
__pycache__/
*.pyc
.env
.vercel/
node_modules/
.DS_Store
```

---

## ✅ Verification Checklist

- [ ] Repository cloned successfully
- [ ] Git status shows clean working tree
- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend server running (http://localhost:8000)
- [ ] Backend server running (http://localhost:5000)
- [ ] API health endpoint responding (HTTP 200)
- [ ] Dashboard loads without errors
- [ ] OpenAPI spec accessible at openapi.yaml
- [ ] Postman collection imports successfully
- [ ] All 5 dashboard views load
- [ ] Browser console shows no errors
- [ ] API requests successful in Postman

---

## 🚀 Next Steps

1. **Explore the Code**
   - Read through `public/dashboard.html` to understand frontend
   - Study `backend/app.py` for backend logic
   - Review `openapi.yaml` for API contracts

2. **Make a Change**
   - Create a feature branch: `git checkout -b feature/test`
   - Modify a file
   - Test locally
   - Commit and push

3. **Test the Pipeline**
   - Prepare 7 test Excel files
   - Use POST /api/upload in Postman
   - Execute pipeline
   - Verify results

4. **Deploy to Production**
   - Test changes thoroughly locally
   - Push to GitHub
   - Verify Vercel deployment (automatic)

---

## 📞 Support

**For issues with local setup:**
1. Check this guide again (most common issues covered)
2. Review GitHub issues: https://github.com/andytrigent/metry360-phase1/issues
3. Check deployment docs: DEPLOYMENT_FINAL.md

**For API issues:**
1. Review openapi.yaml specification
2. Test with Postman collection
3. Check Flask logs for errors
4. Enable Flask debug mode: `FLASK_ENV=development python app.py`

---

**Version**: 1.0  
**Last Updated**: June 23, 2026  
**Maintained By**: Trigent Development Team

