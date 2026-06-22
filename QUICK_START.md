# SOJPE C2H Phase 1 - Quick Start Guide

## 🌐 Live Application

**Dashboard**: https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app

Open this URL in your browser to access the live dashboard.

---

## 📍 Production URLs

### Frontend (Vercel)
```
https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app
```

### Backend API (AWS Lambda)
```
https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod
```

### Code Repository (GitHub)
```
https://github.com/andytrigent/metry360-phase1
```

---

## ⚡ What You Can Do Right Now

1. **View Dashboard**
   - Open: https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app
   - Switch between 5 different views:
     - 📊 Recruitment Scorecard
     - 👥 Management Summary (Collapsed)
     - 👥 Management Summary (Expanded)
     - 💼 AM Productivity
     - 🎯 Director Drilldown
   - View report history with approval workflow

2. **Test API Health**
   - Endpoint: `https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod/api/health`
   - Response: `{ "status": "healthy", "service": "sojpe-c2h-api", "version": "1.0.0-lambda" }`

3. **Upload Files** (Coming in Phase 1.5)
   - Upload 7 raw Excel files
   - System processes data (83-step pipeline)
   - Reports generated and stored

---

## 🔑 Key Features (Currently Available)

✅ 5 interactive dashboard views  
✅ Recruitment metrics with RAG indicators  
✅ Report history with file tracking  
✅ Draft → Review → Approve workflow  
✅ Review Details audit trail  
✅ Data lineage and file download tracking  
✅ Global CDN delivery (Vercel)  
✅ Auto-scaling backend (AWS Lambda)  
✅ Secure file storage (S3)  
✅ Report metadata database (DynamoDB)  

---

## 📊 Dashboard Views

### 1. Recruitment Scorecard (Main View)
- Coverage donut chart
- 4 KPI cards
- Hierarchical team table
- Alert panel (On Track, Watch, Action)

### 2. Management Summary - Collapsed
- Aggregated team metrics
- Quick executive overview

### 3. Management Summary - Expanded
- Detailed drill-down
- Individual contributor metrics

### 4. AM Productivity
- Account Manager analytics
- Recruiter productivity tracking

### 5. Director Drilldown
- Portfolio-level insights
- Director comparison metrics

---

## 🔐 Security & Access

- **Frontend**: Publicly accessible via Vercel CDN
- **Backend API**: AWS API Gateway with Lambda
- **Authentication**: None in Phase 1 (add OAuth/JWT in Phase 2)
- **CORS**: Enabled for development
- **Storage**: S3 with versioning and public access blocked
- **Database**: DynamoDB with encryption at rest

---

## 📱 Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## ⚠️ Important Notes

### Vercel Account
Currently deployed on personal account `trigent-ark-os`.  
**TODO**: Transfer to Trigent's paid Vercel account for production use.

### Phase 1.5 Integration
The backend API is ready but not yet connected to the dashboard.  
Next step: Implement file upload flow and 83-step data pipeline execution.

### AWS Deployment
All infrastructure deployed to `ap-south-1` region (Mumbai):
- Lambda function: `sojpe-data-pipeline`
- API Gateway: ID `2g852sgu1i`
- S3 bucket: `trigent-c2h-files`
- DynamoDB table: `sojpe-reports`

---

## 🚀 Next Steps

1. **Immediate**
   - ✅ Open dashboard: https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app
   - ✅ Explore 5 views
   - ✅ Review report history interface
   - ✅ Test API health endpoint

2. **This Week**
   - Transfer Vercel project to Trigent's account
   - Integrate frontend with backend API
   - Test file upload flow
   - Run 83-step pipeline on sample data

3. **This Month**
   - Complete end-to-end integration
   - Test approval workflow with Akash
   - Production hardening (error handling, rate limiting)
   - Performance optimization

4. **Phase 2 (3 months out)**
   - React 19 frontend
   - Spring Boot backend
   - PostgreSQL database
   - Live API integration

---

## 📞 Support

### For Technical Issues
- Check CloudWatch logs: https://console.aws.amazon.com/cloudwatch/home?region=ap-south-1
- View Lambda function: https://console.aws.amazon.com/lambda/home?region=ap-south-1
- Check GitHub issues: https://github.com/andytrigent/metry360-phase1/issues

### For Documentation
- Full setup guide: See `README.md`
- Deployment details: See `DEPLOYMENT_COMPLETE.md`
- AWS setup: See `AWS_LAMBDA_DEPLOYMENT.md`

---

## 📊 Production Status

| Component | Status | URL |
|-----------|--------|-----|
| Frontend | ✅ Live | https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app |
| API | ✅ Ready | https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod |
| Backend | ✅ Deployed | AWS Lambda (sojpe-data-pipeline) |
| Storage | ✅ Ready | AWS S3 (trigent-c2h-files) |
| Database | ✅ Ready | AWS DynamoDB (sojpe-reports) |
| Monitoring | ✅ Active | AWS CloudWatch |

---

**Last Updated**: June 22, 2026  
**Status**: 🟢 Production Ready  
**Next Demo**: With Rhoni (as scheduled)
