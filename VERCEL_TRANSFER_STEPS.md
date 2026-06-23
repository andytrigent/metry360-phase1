# Vercel Transfer & Custom Domain Setup

**Goal**: Transfer project from personal account to Trigent account + map arkos.studio domain

**Date Started**: June 23, 2026  
**Status**: Ready for execution

---

## Phase 1: Vercel Account Transfer (5 minutes)

### Step 1: Verify Trigent Vercel Account Exists

```bash
# Check if you have access to Trigent's Vercel organization
# If not, you need to:
# 1. Create account at vercel.com
# 2. Create organization "Trigent"
# 3. Add team members

vercel teams list
```

### Step 2: Link to New Organization

```bash
cd D:\experiments\gcc-qmetry\metry360-phase1

# Clear any existing Vercel config
rm -Force .vercel -ErrorAction SilentlyContinue

# Login with Trigent account (or switch if already logged in)
vercel login

# Link project to Trigent organization
vercel link --scope trigent

# When prompted:
# "Found existing project. Link to it?" → NO (we're creating new link)
# "What's your project's name?" → metry360-phase1
# "In which directory is your code located?" → . (current directory)
```

### Step 3: Verify Transfer

```bash
# Check that project is now linked to Trigent
vercel whoami

# Should show Trigent organization name, not personal account

# List projects in Trigent org
vercel projects list --scope trigent
```

---

## Phase 2: Deploy to New Account (2 minutes)

```bash
cd D:\experiments\gcc-qmetry\metry360-phase1

# Full production deployment to Trigent account
vercel --prod --yes --scope trigent
```

**Expected Output**:
```
Vercel CLI
Production: https://metry360-phase1-xxx.vercel.app [NEW URL]
✓ Success
```

**Save this URL** - this is your new production URL on Trigent account.

---

## Phase 3: Configure Custom Domain (arkos.studio) - 10 minutes

### Step 1: Add Domain in Vercel Dashboard

```bash
# Via CLI (easiest)
vercel domains add arkos.studio --scope trigent

# OR via Vercel Dashboard:
# 1. Go to https://vercel.com/dashboard
# 2. Project → Settings → Domains
# 3. Add Domain: arkos.studio
```

### Step 2: Get DNS Configuration

Vercel will show you DNS records to add. Typically:

```
For arkos.studio:
Type: A Record
Name: @
Value: 76.76.19.165

OR

Type: CNAME Record
Name: www
Value: cname.vercel-dns.com
```

**Note down these values** - you'll need them for DNS provider.

### Step 3: Update DNS Provider

Log in to your DNS provider (GoDaddy, Cloudflare, Route53, etc.) and add:

**If using A Record:**
```
Type:  A
Name:  @ (or arkos.studio)
Value: 76.76.19.165
TTL:   3600
```

**If using CNAME Record:**
```
Type:  CNAME
Name:  www
Value: cname.vercel-dns.com
TTL:   3600
```

### Step 4: Verify DNS Configuration

```bash
# Check DNS propagation
nslookup arkos.studio

# Or with dig:
dig arkos.studio

# Should resolve to Vercel's IP/CNAME
```

### Step 5: Verify in Vercel

```bash
# Check domain status
vercel domains inspect arkos.studio --scope trigent

# Status should show: ✓ Valid Configuration
```

---

## Complete Command Sequence

Run these commands in order:

```bash
# Navigate to project
cd D:\experiments\gcc-qmetry\metry360-phase1

# Step 1: Clear old config
rm -Force .vercel -ErrorAction SilentlyContinue

# Step 2: Login to Trigent account
vercel login

# Step 3: Link to Trigent (create new link)
vercel link --scope trigent

# Step 4: Deploy to production
vercel --prod --yes --scope trigent

# Step 5: Add custom domain
vercel domains add arkos.studio --scope trigent

# Step 6: Verify setup
vercel domains inspect arkos.studio --scope trigent

# Step 7: Check DNS (wait 1-2 minutes, then run):
nslookup arkos.studio
```

---

## DNS Propagation Timeline

| Time | Status |
|------|--------|
| Immediately | Vercel configures endpoints |
| 1-5 min | DNS cache updates |
| 5-30 min | Most ISPs resolve correctly |
| 1-48 hours | Global propagation complete |

**During propagation**, site will gradually become available across regions.

---

## Troubleshooting

### Domain shows "Invalid Configuration"
- **Check**: DNS records in provider are correct
- **Wait**: DNS can take 10-30 minutes to propagate
- **Verify**: Use `nslookup arkos.studio` to test
- **Solution**: Run `vercel domains refresh arkos.studio --scope trigent`

### Still seeing old URL in browser
- **Clear**: Browser cache (Ctrl+Shift+Delete)
- **Flush**: DNS cache:
  ```bash
  ipconfig /flushdns
  ```
- **Wait**: May take up to 24 hours for full propagation

### DNS provider doesn't show Vercel records
- **Check**: You're editing the correct domain
- **Verify**: Records are saved (some providers require explicit save)
- **Look for**: A records or CNAME records section
- **Wait**: 5-15 minutes for changes to apply

### arkos.studio works but www.arkos.studio doesn't
- **Add**: A or CNAME record for `www` subdomain
- **Or**: Use `vercel domains add www.arkos.studio --scope trigent`

---

## Verification Steps

After all setup complete, verify:

```bash
# 1. Check Vercel project linked
vercel whoami --scope trigent
# Should show: Trigent organization

# 2. Check domain configured
vercel domains list --scope trigent
# Should show: arkos.studio with status ✓

# 3. Check DNS resolution
nslookup arkos.studio
# Should show Vercel's IP

# 4. Test in browser
# Open: https://arkos.studio
# Should load dashboard

# 5. Check SSL certificate
# Browser should show 🔒 Secure
# No certificate warnings
```

---

## Environment Variables (Update if needed)

If you use environment variables in Vercel:

```bash
# Set environment variables
vercel env add API_BASE_URL --scope trigent
# Value: https://2g852sgu1i.execute-api.ap-south-1.amazonaws.com/prod

vercel env add AWS_REGION --scope trigent
# Value: ap-south-1

# Redeploy to apply
vercel --prod --yes --scope trigent
```

---

## Post-Transfer Documentation Updates

After successful transfer, update files:

```bash
# Edit README.md
# Change: https://metry360-phase1-evl2ll827-trigent-ark-os.vercel.app
# To:     https://arkos.studio

# Edit QUICK_START.md
# Change all URLs to use arkos.studio

# Commit changes
git add README.md QUICK_START.md
git commit -m "Update documentation to use arkos.studio custom domain"
git push origin main
```

---

## Final Checklist

- [ ] Trigent Vercel account created
- [ ] Vercel CLI logged in to Trigent account
- [ ] Project linked to Trigent (`vercel link --scope trigent`)
- [ ] Deployed to production (`vercel --prod --yes --scope trigent`)
- [ ] arkos.studio domain added to Vercel
- [ ] DNS records added to DNS provider
- [ ] DNS propagated (tested with nslookup)
- [ ] SSL certificate auto-generated and valid
- [ ] https://arkos.studio loads dashboard
- [ ] Documentation updated with new URL
- [ ] Team notified of new URL

---

## Timeline

| Task | Time | Status |
|------|------|--------|
| Account setup | Immediate | Ready |
| Project transfer | 5 min | Ready |
| Production deploy | 2 min | Ready |
| Domain config | 5 min | Ready |
| DNS propagation | 5-30 min | Automatic |
| SSL cert | Auto | Automatic |
| **Total** | **20 min** | **Ready to go** |

---

## Support

**If transfer fails**:
- Check Vercel dashboard for errors
- Review CLI output carefully
- Try again with: `vercel --prod --force --scope trigent`

**If domain doesn't work**:
- Wait 30 minutes for DNS propagation
- Check DNS provider shows correct records
- Test with: `nslookup arkos.studio` or `dig arkos.studio`

**Need help**:
- Vercel docs: https://vercel.com/docs
- DNS docs: https://vercel.com/docs/custom-domains

---

**Ready to execute? Start with Step 1 above.**

Once complete, the dashboard will be live at: **https://arkos.studio**
