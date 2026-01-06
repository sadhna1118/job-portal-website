# 🚀 Quick Start - Deploy to GitHub

**Admin: Sadhna**

Follow these simple steps to get your Job Portal on GitHub:

## Step 1: Open PowerShell
Navigate to your project folder:
```powershell
cd "c:\Users\HP\OneDrive\Documents\Desktop\job portal web"
```

## Step 2: Initialize Git
```powershell
git init
git add .
git commit -m "Initial commit: Job Portal by Sadhna"
```

## Step 3: Create GitHub Repository
1. Go to https://github.com
2. Click **"+"** → **"New repository"**
3. Name: `job-portal-web`
4. Description: `Job Portal by Sadhna - Flask & Tailwind CSS`
5. Make it **Public** or **Private**
6. **DON'T** check "Initialize with README"
7. Click **"Create repository"**

## Step 4: Push to GitHub
Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/job-portal-web.git
git branch -M main
git push -u origin main
```

**Note**: Use Personal Access Token instead of password when prompted.

## Step 5: Get Your Token (If Needed)
1. GitHub.com → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. "Generate new token (classic)"
4. Name: "Job Portal"
5. Check: `repo` (all checkboxes under it)
6. Click "Generate token"
7. **Copy the token** (you won't see it again!)
8. Use this token as password when pushing

## 🎉 Done!
Your code is now on GitHub at:
```
https://github.com/YOUR_USERNAME/job-portal-web
```

---

## Next: Deploy Live

### Easy Option - Render (Free)
1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service
4. Select your `job-portal-web` repo
5. Settings:
   - Build: `pip install -r requirements.txt && npm install && npm run build:css`
   - Start: `gunicorn app:app`
6. Add environment variable:
   - `SECRET_KEY` = (any random 32-character string)
7. Create Web Service
8. Wait 5-10 minutes
9. Your app is live! 🚀

---

For detailed instructions, see `GITHUB_DEPLOYMENT.md`