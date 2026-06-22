# Vercel Account Transfer Guide

## Current Status

**Current Deployment**: 
- URL: https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app
- Account: Personal (trigent-ark-os)
- Status: ✅ Working but on wrong account

**Target Deployment**:
- Account: Trigent's paid Vercel account
- Billing: Trigent organization
- Team access: Full team visibility

---

## Option 1: Transfer Existing Project (Recommended)

### Step 1: Contact Vercel Support
```
Email: support@vercel.com
Subject: Transfer Project to Organization

Message:
"Please transfer the following project:
- Project: metry360-phase1
- Current Account: trigent-ark-os
- Target Organization: Trigent (provide your organization ID)
- Reason: Moving to official company account for production

Thank you"
```

### Step 2: Provide Project Details
- Project ID: Found in Vercel project settings
- Current URL: https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app
- GitHub Repository: https://github.com/andytrigent/metry360-phase1

### Step 3: Update Local Environment
```bash
# After transfer is complete:
cd D:\experiments\gcc-qmetry\metry360-phase1

# Redeploy to new account
vercel --prod --yes --scope trigent-organization-name
```

---

## Option 2: Create New Project on Trigent Account

### Step 1: Invite to Vercel
1. Log in to Vercel with Trigent account
2. Settings → Team → Invite member
3. Invite your email address
4. Accept invitation

### Step 2: Create New Project
```bash
# In Vercel dashboard:
1. Click "Add New..." → Project
2. Select GitHub repo: metry360-phase1
3. Framework: Other (static)
4. Build Command: echo 'Static site'
5. Output Directory: public/
6. Deploy
```

### Step 3: Deploy via CLI
```bash
cd D:\experiments\gcc-qmetry\metry360-phase1

# Login with Trigent account
vercel login

# Deploy to Trigent account
vercel --prod --yes --scope trigent-account-name
```

---

## Option 3: Complete Fresh Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/andytrigent/metry360-phase1.git
cd metry360-phase1
```

### Step 2: Link to New Vercel Project
```bash
# Create new project on Trigent's Vercel
vercel --prod --yes --scope trigent-account-name
```

### Step 3: Configure Environment
In Vercel Dashboard → Settings → Environment Variables:
```
API_BASE_URL = https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod
AWS_REGION = ap-south-1
```

### Step 4: Update DNS (if using custom domain)
1. Add custom domain in Vercel
2. Update DNS provider with CNAME records
3. Verify domain ownership

---

## Post-Transfer Checklist

- [ ] Project successfully transferred/deployed to Trigent account
- [ ] URL is accessible from Trigent's domain
- [ ] GitHub integration still working
- [ ] Environment variables configured
- [ ] API endpoint accessible from frontend
- [ ] CloudWatch logs showing traffic
- [ ] SSL/TLS certificate auto-generated
- [ ] Team members added to Vercel project
- [ ] Billing configured in Trigent account
- [ ] CI/CD pipeline working

---

## Vercel Pro Plan Features (Recommended)

**Cost**: $20/month

**Includes**:
- ✅ Priority support
- ✅ Team collaboration
- ✅ Advanced analytics
- ✅ Custom domains
- ✅ Unlimited deployments
- ✅ Preview environments
- ✅ Automatic Git deployments

---

## Troubleshooting

### Project not showing in new account
- Check you're logged into correct Vercel account
- Verify GitHub repository is properly connected
- Ensure GitHub user is admin of repository

### Environment variables not working
- Variables must be set in Vercel dashboard
- Redeploy after adding variables
- Check variable names match frontend code

### Domain not resolving
- DNS records may take 24-48 hours to propagate
- Verify CNAME/A records in DNS provider
- Test with dig/nslookup:
  ```bash
  nslookup yourdomain.com
  dig yourdomain.com CNAME
  ```

### Build or deployment failing
- Check build logs in Vercel dashboard
- Verify outputDirectory is set to `public/`
- Ensure no Python/backend files in public folder

---

## Current AWS Deployment (No Changes Needed)

AWS resources remain deployed and don't need to move:
- ✅ Lambda: sojpe-data-pipeline (ap-south-1)
- ✅ API Gateway: 2g852sgu1i (ap-south-1)
- ✅ S3: trigent-c2h-files (ap-south-1)
- ✅ DynamoDB: sojpe-reports (ap-south-1)

Frontend just needs to point to: `https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod`

---

## Timeline

| Step | Duration | Status |
|------|----------|--------|
| Request Transfer | Immediate | ✅ Ready |
| Vercel Processing | 24-48 hours | ⏳ Pending |
| DNS Propagation | 24-48 hours | ⏳ Pending |
| Verification | 1 hour | ⏳ Pending |
| **Total** | **2-3 days** | |

---

## Contact Information

**Vercel Support**:
- Email: support@vercel.com
- Status Page: https://vercel-status.com

**GitHub Integration Support**:
- Documentation: https://vercel.com/docs/git/github

**Account Issues**:
- Billing: billing@vercel.com
- Security: security@vercel.com

---

## Important Notes

1. **Billing**: After transfer, Trigent account will be billed
2. **Team Access**: All team members need Vercel accounts for collaboration
3. **Custom Domain**: If using custom domain, DNS must be updated
4. **Backups**: Existing deployment continues to work during transfer
5. **CI/CD**: GitHub Actions automatically re-trigger on transfer completion

---

## After Transfer

Once transferred to Trigent account, update documentation:
1. Update README.md with new URL
2. Update QUICK_START.md with new URL
3. Notify all users of new URL
4. Update any external integrations

**New URL Pattern**: `https://metry360-phase1.trigent.com` or `https://sojpe-dashboard.vercel.app`

---

**Status**: Ready for transfer  
**Current Account**: trigent-ark-os (personal)  
**Target Account**: Trigent (organization)  
**Next Step**: Contact Vercel support to initiate transfer
