# 🚀 GitHub Deployment Guide

Complete guide to deploy your Job Portal project to GitHub and make it publicly available.

**Admin/Owner**: Sadhna

## 📋 Prerequisites

- Git installed on your computer
- GitHub account created (free at https://github.com)
- Project files ready in your local directory

## 🔧 Step 1: Prepare Your Project

### ✅ Admin Credentials Updated
Admin name has been updated to **"Sadhna"**

### Security Updates Before Deployment
1. **Never commit sensitive data** to GitHub:
   - Database files (already in `.gitignore`)
   - `.env` files with passwords
   - Upload folders with user data

2. **Update passwords in production** (after deployment):
   ```
   Admin (Sadhna): admin123 → [strong-password]
   Recruiters: recruiter123 → [strong-password]
   Job Seekers: seeker123 → [strong-password]
   ```

## 📁 Step 2: Initialize Git Repository

Open PowerShell in your project directory and run:

```powershell
# Navigate to your project
cd "c:\Users\HP\OneDrive\Documents\Desktop\job portal web"

# Initialize Git repository
git init

# Add all files to staging
git add .

# Create first commit
git commit -m "Initial commit: Job Portal by Sadhna"
```

## 🌐 Step 3: Create GitHub Repository

### Option A: Using GitHub Website
1. Go to https://github.com
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in repository details:
   - **Repository name**: `job-portal-web`
   - **Description**: `Professional job search platform built with Flask and Tailwind CSS - Admin: Sadhna`
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README (you already have one)
4. Click **"Create repository"**

### Option B: Using GitHub CLI (if installed)
```powershell
gh repo create job-portal-web --public --source=. --remote=origin --description "Job Portal by Sadhna"
```

## 🔗 Step 4: Connect Local Repository to GitHub

After creating the GitHub repository, GitHub will show you commands. Run these:

```powershell
# Add GitHub as remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/job-portal-web.git

# Verify remote was added
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

**If you encounter authentication issues:**
- GitHub no longer accepts passwords for Git operations
- You need to create a **Personal Access Token (PAT)**:
  1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  2. Click "Generate new token (classic)"
  3. Give it a name: "Job Portal Deploy"
  4. Select scopes: `repo` (full control of repositories)
  5. Click "Generate token"
  6. **Copy the token immediately** (you won't see it again!)
  7. Use this token as your password when Git asks for credentials

## 🎯 Step 5: Verify Deployment

1. Go to your GitHub repository URL:
   ```
   https://github.com/YOUR_USERNAME/job-portal-web
   ```

2. Check that all files are uploaded:
   - ✅ `app.py`, `seed_data.py`, `run.py`
   - ✅ `templates/` folder with all HTML files
   - ✅ `static/` folder with CSS and JS
   - ✅ `requirements.txt`, `package.json`
   - ✅ `README.md`, `.gitignore`, `.env.example`
   - ✅ Documentation files (CONTRIBUTING.md, DEPLOYMENT_GUIDE.md, etc.)
   - ❌ No `instance/` folder (correctly ignored)
   - ❌ No `.env` file (correctly ignored)
   - ❌ No `node_modules/` (correctly ignored)
   - ❌ No `uploads/` (correctly ignored)

## 📝 Step 6: Enhance Your Repository

### Add Repository Description and Topics
1. Go to repository → Click **"About"** (gear icon on right side)
2. **Description**: 
   ```
   Professional job search platform with Flask, SQLAlchemy & Tailwind CSS v4. Features job posting, application tracking, and recruiter management. Owner: Sadhna
   ```
3. **Website**: Add your deployment URL (after Step 9)
4. **Topics** (click to add):
   - `flask`
   - `python`
   - `job-portal`
   - `tailwindcss`
   - `sqlalchemy`
   - `web-application`
   - `recruitment`
   - `job-search`

### Optional: Add Badges to README
You can add these at the top of your README.md:

```markdown
[![Owner](https://img.shields.io/badge/Owner-Sadhna-blue?style=flat-square)](https://github.com/YOUR_USERNAME)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-v4-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
```

## 🔄 Step 7: Making Updates

After making changes to your code:

```powershell
# Check status of changed files
git status

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Update: Description of changes"

# Push to GitHub
git push origin main
```

### Common Commit Message Examples
```
feat: Add email notification feature
fix: Resolve login authentication issue
update: Improve dashboard UI
docs: Update README with new instructions
style: Format code with black
```

### Common Git Commands

```powershell
# View commit history
git log --oneline

# View recent commits
git log --oneline -10

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard

# Create a new branch
git checkout -b feature/new-feature

# Switch back to main branch
git checkout main

# Pull latest changes from GitHub
git pull origin main

# View current branch
git branch

# Delete a branch
git branch -d branch-name
```

## 🚀 Step 8: Deploy Live Application

GitHub hosts code, but to run the Flask app live, use these platforms:

### Option A: Render (✅ Recommended - Free Tier)
1. Go to https://render.com
2. Sign up with your GitHub account
3. Click **"New +"** → **"Web Service"**
4. Click **"Connect account"** and authorize GitHub
5. Select your `job-portal-web` repository
6. Configure:
   - **Name**: `job-portal-sadhna`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && npm install && npm run build:css
     ```
   - **Start Command**: 
     ```
     gunicorn app:app
     ```
   - **Instance Type**: Free
7. Click **"Advanced"** and add environment variables:
   - `SECRET_KEY`: Generate random string (use online generator)
   - `FLASK_ENV`: `production`
   - `DATABASE_URL`: (Render will provide PostgreSQL URL if you add database)
8. Click **"Create Web Service"**
9. Wait for deployment (5-10 minutes)
10. Click the URL to view your live app!

**To Add Database on Render:**
- Go to Dashboard → **"New +"** → **"PostgreSQL"**
- Connect it to your web service
- Update `app.py` to use PostgreSQL instead of SQLite

### Option B: Railway (Free Tier Available)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects Flask and sets it up
6. Add environment variables in **"Variables"** tab
7. Click **"Deploy"**
8. Get your deployment URL from **"Settings"** → **"Domains"**

### Option C: PythonAnywhere (Free Tier Available)
1. Go to https://www.pythonanywhere.com
2. Create a free account
3. Go to **"Web"** tab → **"Add a new web app"**
4. Choose **"Manual configuration"** → **"Python 3.10"**
5. In **"Code"** section:
   - Clone your repo: `git clone https://github.com/YOUR_USERNAME/job-portal-web.git`
6. Set up virtual environment
7. Configure WSGI file
8. Install dependencies: `pip install -r requirements.txt`
9. Reload web app

### Option D: Heroku (Requires payment)
See `DEPLOYMENT_GUIDE.md` for detailed Heroku instructions

## 🗄️ Step 9: Database for Production

For production, replace SQLite with PostgreSQL:

### Update app.py for PostgreSQL:
```python
import os

# In app.py, update database URI:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///jobportal.db'

# Fix for PostgreSQL (Heroku/Render use postgres:// which needs to be postgresql://)
uri = app.config['SQLALCHEMY_DATABASE_URI']
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
```

### Initialize Database on Production:
After deployment, run these commands on your hosting platform:

```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Database created!")
```

Then run seed script:
```bash
python seed_data.py
```

## 🛡️ Security Checklist for Production

Before going live:
- [ ] Change `SECRET_KEY` to secure random value
- [ ] Set `DEBUG=False` in production
- [ ] Change all default passwords
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up database backups
- [ ] Configure proper CORS if needed
- [ ] Add rate limiting for API endpoints
- [ ] Enable CSRF protection

## 📊 Step 10: Repository Management

### Create Releases
1. Go to repository → **"Releases"**
2. Click **"Create a new release"**
3. Tag: `v1.0.0`
4. Title: `Job Portal v1.0 - Initial Release`
5. Description: List features
6. Click **"Publish release"**

### Add LICENSE
1. Go to repository → **"Add file"** → **"Create new file"**
2. Name it `LICENSE`
3. GitHub will show "Choose a license template"
4. Select **MIT License** (recommended for open source)
5. Replace `[year]` with 2026 and `[fullname]` with "Sadhna"
6. Commit the file

### Create Issues
Set up issue templates:
1. Go to **"Settings"** → **"Features"** → Enable **"Issues"**
2. Create templates for:
   - Bug reports
   - Feature requests
   - Questions

### Enable Discussions (Optional)
For community engagement:
- Go to **"Settings"** → **"Features"** → Enable **"Discussions"**

## 🎓 Best Practices

### Branch Protection
1. Go to **"Settings"** → **"Branches"**
2. Add rule for `main` branch
3. Enable:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Include administrators

### Collaborators
1. Go to **"Settings"** → **"Collaborators"**
2. Click **"Add people"**
3. Enter GitHub username or email
4. Choose permission level (Read/Write/Admin)

### GitHub Actions (CI/CD)
Create `.github/workflows/test.yml` for automated testing:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## 📞 Troubleshooting

### "Permission denied (publickey)"
Generate and add SSH key:
```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
Get-Content ~/.ssh/id_ed25519.pub | clip

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

### "Failed to push some refs"
```powershell
# Pull latest changes first
git pull origin main --rebase
git push origin main
```

### Large Files Error (>100MB)
```powershell
# Remove file from Git history
git rm --cached path/to/large/file

# Add to .gitignore
echo "path/to/large/file" >> .gitignore

# Commit changes
git commit -m "Remove large file"
git push origin main
```

### Merge Conflicts
```powershell
# Update your local repository
git pull origin main

# Git will show conflicts
# Open conflicting files and resolve manually
# Look for markers: <<<<<<< HEAD, =======, >>>>>>> 

# After resolving, stage changes
git add .

# Commit resolution
git commit -m "Resolve merge conflicts"

# Push changes
git push origin main
```

## ✅ Deployment Checklist

- [ ] Git repository initialized locally
- [ ] Admin name updated to "Sadhna" ✅
- [ ] `.gitignore` configured properly ✅
- [ ] `.env.example` created (no real passwords) ✅
- [ ] README.md updated with admin info
- [ ] GitHub repository created
- [ ] Code pushed to GitHub successfully
- [ ] Repository description and topics added
- [ ] README badges added (optional)
- [ ] LICENSE file added
- [ ] Production hosting platform chosen
- [ ] Environment variables configured on hosting
- [ ] Database initialized on production
- [ ] Admin password changed on production
- [ ] Application tested on live URL
- [ ] Custom domain configured (optional)

## 📚 Useful Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Desktop](https://desktop.github.com/) - GUI alternative
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Flask Deployment](https://flask.palletsprojects.com/en/3.0.x/deploying/)

## 🎉 Next Steps

After successful deployment:

1. **Share Your Project**:
   - Add repository link to your resume/portfolio
   - Share on LinkedIn with #Flask #Python #WebDev
   - Post on Twitter/X with screenshots

2. **Get Feedback**:
   - Ask friends/colleagues to test
   - Post on Reddit (r/flask, r/Python)
   - Share in developer communities

3. **Continuous Improvement**:
   - Monitor error logs
   - Fix bugs reported by users
   - Add new features
   - Improve performance
   - Enhance security

4. **Build Your Profile**:
   - Star interesting repositories
   - Contribute to open source
   - Create more projects
   - Write technical blog posts

---

**Congratulations! 🎉**

Your Job Portal is now on GitHub and accessible to the world!

**Repository Owner**: Sadhna
**Project**: Job Portal Web Application
**Tech Stack**: Flask + SQLAlchemy + Tailwind CSS v4

Remember to update passwords before sharing with real users!