# 🚀 DEPLOY YOUR JOB PORTAL LIVE NOW

**Admin: Sadhna**
**Repository**: https://github.com/sadhna1118/job-portal-website

✅ **YOUR CODE IS NOW ON GITHUB!**

---

## 🌐 Deploy Live on Render (FREE) - 10 Minutes

### Step 1: Go to Render
Open your browser and go to: **https://render.com**

### Step 2: Sign Up with GitHub
1. Click **"Get Started for Free"**
2. Click **"Sign up with GitHub"**
3. Authorize Render to access your GitHub account
4. This automatically connects your repositories

### Step 3: Create New Web Service
1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if needed
4. Find and select: **sadhna1118/job-portal-website**
5. Click **"Connect"**

### Step 4: Configure Your Service
Fill in these settings:

**Name**: `job-portal-sadhna` (or any name you like)

**Region**: Select closest to you (e.g., Singapore, Oregon, Frankfurt)

**Branch**: `main`

**Root Directory**: Leave blank

**Runtime**: `Python 3`

**Build Command**: 
```
pip install -r requirements.txt && npm install && npm run build:css
```

**Start Command**:
```
gunicorn app:app
```

**Instance Type**: Select **"Free"** (at the bottom)

### Step 5: Add Environment Variables
Click **"Advanced"** button, then click **"Add Environment Variable"**

Add these variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `your-super-secret-random-key-change-this-123456789` |
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.0` |

**Important**: For SECRET_KEY, use a random string. You can generate one here:
- Go to https://djecrety.ir/ and copy a random key
- Or use any random 32+ character string

### Step 6: Create Web Service
1. Scroll down and click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Render will:
   - Install Python dependencies
   - Install Node.js dependencies
   - Build CSS with Tailwind
   - Start your application

### Step 7: View Your Live App! 🎉
1. Once deployment is complete (green ✓), you'll see your app URL
2. It will look like: `https://job-portal-sadhna.onrender.com`
3. Click the URL to open your live app!

---

## 🗄️ Add Database (PostgreSQL)

Your app currently uses SQLite which won't persist on Render. Add PostgreSQL:

### Step 1: Create PostgreSQL Database
1. Go to Render Dashboard
2. Click **"New +"** → **"PostgreSQL"**
3. Name: `job-portal-db`
4. Database: `jobportal`
5. User: `jobportal_user`
6. Region: Same as your web service
7. Instance Type: **"Free"**
8. Click **"Create Database"**

### Step 2: Connect Database to Web Service
1. Wait for database to be ready (2-3 minutes)
2. Go to your database → **"Info"** tab
3. Copy the **"Internal Database URL"**
4. Go to your web service → **"Environment"** tab
5. Add new environment variable:
   - Key: `DATABASE_URL`
   - Value: [paste the internal database URL]
6. Click **"Save Changes"**

### Step 3: Update app.py for PostgreSQL
The code needs a small update. I'll do this for you: