# 🚀 Deployment Guide - Job Portal

This guide provides step-by-step instructions for deploying the Job Portal application to production.

## 📋 Pre-Deployment Checklist

### Security
- [ ] Change `SECRET_KEY` to a cryptographically secure random string
- [ ] Update all default passwords (admin, demo accounts)
- [ ] Set `DEBUG=False` in production
- [ ] Enable `SESSION_COOKIE_SECURE=True` (requires HTTPS)
- [ ] Configure CORS if needed
- [ ] Set up rate limiting
- [ ] Enable CSRF protection for forms

### Database
- [ ] Switch from SQLite to PostgreSQL/MySQL
- [ ] Set up regular database backups
- [ ] Configure database connection pooling
- [ ] Set up database migrations with Flask-Migrate

### File Storage
- [ ] Move uploaded files to cloud storage (AWS S3, Cloudflare R2)
- [ ] Set up CDN for static assets
- [ ] Configure file size limits
- [ ] Implement virus scanning for uploads

### Monitoring
- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Configure logging (CloudWatch, Papertrail)
- [ ] Set up uptime monitoring
- [ ] Configure performance monitoring

## 🌐 Deployment Options

### Option 1: Heroku (Easiest)

#### Step 1: Prepare Files

**Procfile:**
```
web: gunicorn app:app
```

**runtime.txt:**
```
python-3.11.0
```

#### Step 2: Deploy
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-job-portal

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Run migrations
heroku run python
>>> from app import db
>>> db.create_all()
>>> exit()

# Seed data (optional)
heroku run python seed_data.py

# Open app
heroku open
```

### Option 2: DigitalOcean App Platform

#### Step 1: Configure App

Create `app.yaml`:
```yaml
name: job-portal
services:
  - name: web
    source_dir: /
    github:
      repo: yourusername/job-portal
      branch: main
    build_command: |
      pip install -r requirements.txt
      npm install
      npm run build:css
    run_command: gunicorn --workers 4 app:app
    instance_size_slug: basic-xxs
    envs:
      - key: SECRET_KEY
        scope: RUN_TIME
        value: ${SECRET_KEY}
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}
    http_port: 8080
databases:
  - name: jobportal-db
    engine: PG
    version: "14"
```

#### Step 2: Deploy
1. Connect GitHub repository
2. Configure environment variables
3. Deploy automatically on push

### Option 3: AWS EC2 (Advanced)

#### Step 1: Launch EC2 Instance
```bash
# Ubuntu 22.04 LTS
# t2.micro or larger
```

#### Step 2: SSH and Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Create application directory
sudo mkdir -p /var/www/jobportal
sudo chown $USER:$USER /var/www/jobportal
cd /var/www/jobportal

# Clone repository (or upload files)
git clone <your-repo> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Install Node packages and build CSS
npm install
npm run build:css

# Set up PostgreSQL
sudo -u postgres createdb jobportal
sudo -u postgres createuser jobportal_user
sudo -u postgres psql
postgres=# ALTER USER jobportal_user WITH PASSWORD 'secure_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE jobportal TO jobportal_user;
postgres=# \q

# Configure environment
nano .env
# Add:
# SECRET_KEY=your-secret-key
# DATABASE_URL=postgresql://jobportal_user:secure_password@localhost/jobportal
# FLASK_ENV=production

# Initialize database
python run.py
# Or manually:
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

#### Step 3: Configure Gunicorn

**Create systemd service** `/etc/systemd/system/jobportal.service`:
```ini
[Unit]
Description=Job Portal Gunicorn Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/jobportal
Environment="PATH=/var/www/jobportal/venv/bin"
EnvironmentFile=/var/www/jobportal/.env
ExecStart=/var/www/jobportal/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:jobportal.sock \
    --access-logfile /var/log/jobportal/access.log \
    --error-logfile /var/log/jobportal/error.log \
    app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/jobportal
sudo chown ubuntu:www-data /var/log/jobportal

# Start service
sudo systemctl start jobportal
sudo systemctl enable jobportal
sudo systemctl status jobportal
```

#### Step 4: Configure Nginx

**Create** `/etc/nginx/sites-available/jobportal`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/jobportal/jobportal.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/jobportal/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /var/www/jobportal/uploads;
        internal;
    }

    client_max_body_size 5M;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/jobportal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 5: SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
sudo systemctl reload nginx
```

### Option 4: Render (Modern Platform)

#### Step 1: Configure

**render.yaml:**
```yaml
services:
  - type: web
    name: jobportal
    env: python
    buildCommand: |
      pip install -r requirements.txt
      npm install
      npm run build:css
    startCommand: gunicorn app:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: jobportal-db
          property: connectionString
      - key: PYTHON_VERSION
        value: 3.11.0

databases:
  - name: jobportal-db
    databaseName: jobportal
    user: jobportal
```

#### Step 2: Deploy
1. Connect GitHub repository
2. Render auto-deploys on push
3. Database created automatically

## 🔧 Environment Configuration

### Production Environment Variables

```bash
# Application
SECRET_KEY=<generate-with-python-secrets>
FLASK_ENV=production
DEBUG=False

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Session
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# File Storage
UPLOAD_FOLDER=/var/uploads
MAX_CONTENT_LENGTH=5242880

# Email (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# External Services
SENTRY_DSN=<your-sentry-dsn>
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
S3_BUCKET=jobportal-uploads
```

### Generate Secure Secret Key

```python
import secrets
print(secrets.token_urlsafe(32))
```

## 📊 Database Migration

### Switch to PostgreSQL

**Update app.py:**
```python
# Install: pip install psycopg2-binary

# Update connection string
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Handle Heroku postgres:// prefix
uri = os.environ.get('DATABASE_URL')
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
```

### Export Data from SQLite

```python
# Export to JSON
import json
from app import app, db, User, Job, Application

with app.app_context():
    users = [{'username': u.username, 'email': u.email, ...} 
             for u in User.query.all()]
    
    with open('users.json', 'w') as f:
        json.dump(users, f)
```

## 🔒 Security Best Practices

### 1. Strong Secret Key
```python
import secrets
SECRET_KEY = secrets.token_urlsafe(32)
```

### 2. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ...
```

### 3. HTTPS Only
```python
from flask_talisman import Talisman

if not app.debug:
    Talisman(app, force_https=True)
```

### 4. Input Validation
```python
from wtforms import Form, StringField, validators

class JobForm(Form):
    title = StringField('Title', [
        validators.Length(min=3, max=200),
        validators.DataRequired()
    ])
```

## 📈 Performance Optimization

### 1. Database Indexing
```python
# Add indexes to frequently queried columns
class Job(db.Model):
    __table_args__ = (
        db.Index('idx_job_status', 'status'),
        db.Index('idx_job_created', 'created_at'),
    )
```

### 2. Caching
```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

@app.route('/jobs')
@cache.cached(timeout=300)
def jobs():
    # ...
```

### 3. CDN for Static Assets
```html
<!-- Use CDN for static files -->
<link rel="stylesheet" href="https://cdn.example.com/css/output.css">
```

## 🔄 Continuous Deployment

### GitHub Actions Example

**.github/workflows/deploy.yml:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          npm install
          npm run build:css
      
      - name: Run tests
        run: pytest
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-job-portal"
          heroku_email: "your-email@example.com"
```

## 🆘 Troubleshooting

### Common Issues

**502 Bad Gateway:**
- Check Gunicorn is running: `sudo systemctl status jobportal`
- Check Nginx config: `sudo nginx -t`
- Check logs: `tail -f /var/log/nginx/error.log`

**Database Connection Error:**
- Verify DATABASE_URL is correct
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Test connection: `psql -h localhost -U jobportal_user -d jobportal`

**Static Files Not Loading:**
- Run: `npm run build:css`
- Check Nginx static file configuration
- Verify file permissions: `ls -la static/`

## 📚 Additional Resources

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [Nginx Configuration Best Practices](https://www.nginx.com/resources/wiki/start/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

---

**Need help?** Open an issue in the repository!