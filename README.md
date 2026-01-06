# 💼 Job Portal - Professional Job Search Platform
http://127.0.0.1:5000/jobs

[![Owner](https://img.shields.io/badge/Admin-Sadhna-blue?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-v4-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

A fully functional, production-ready job portal web application built with Flask, SQLAlchemy, and Tailwind CSS v4. This platform connects talented job seekers with top employers, featuring a modern UI, comprehensive job search, application tracking, and recruiter management tools.

**Admin/Owner**: Sadhna

## ✨ Key Features

### 🎯 For Job Seekers
- 🔍 **Advanced Job Search** - Search and filter by title, location, job type, experience level, and salary
- 📝 **Quick Applications** - Apply with cover letters and resume uploads (PDF, DOC, DOCX)
- 📊 **Application Tracking** - Monitor status (pending, reviewed, accepted, rejected) in real-time
- 💾 **Save Jobs** - Bookmark interesting positions for later review
- 🎨 **Personalized Dashboard** - View all applications and saved jobs in one place
- 🔔 **Similar Jobs** - Discover related opportunities on job detail pages

### 👔 For Recruiters
- ✍️ **Post Jobs** - Create detailed listings with requirements, skills, and salary ranges
- 📝 **Edit/Delete Postings** - Full control over job listings
- 👥 **Application Management** - Review applications and update candidate statuses
- 📈 **Applicant Tracking** - See detailed applicant information including cover letters
- 🎯 **Job Performance** - Track number of applications per posting

### 🔐 For Administrators
- 📊 **Analytics Dashboard** - Real-time statistics on users, jobs, and applications
- 👤 **User Management** - View and monitor all registered users
- 💼 **Job Oversight** - Manage all job postings across the platform
- 📈 **Platform Insights** - Track active jobs and total applications

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Jinja2 Templates, Tailwind CSS v4
- **Database**: SQLite
- **Authentication**: Flask-Login with password hashing
- **Icons**: Lucide Icons

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js 14+ and npm (for Tailwind CSS)
- Git (optional)

### Installation Steps

1. **Navigate to Project Directory**
   ```bash
   cd "c:\Users\HP\OneDrive\Documents\Desktop\job portal web"
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node Dependencies** (for Tailwind CSS)
   ```bash
   npm install
   ```

4. **Build CSS Assets**
   ```bash
   npm run build:css
   ```

5. **Seed Sample Data** (Recommended for testing)
   ```bash
   python seed_data.py
   ```
   This creates:
   - 10 recruiters from major companies
   - 12 job seekers
   - 70+ diverse job postings
   - Sample applications and saved jobs

6. **Run the Application**
   ```bash
   python run.py
   ```
   Or use the original:
   ```bash
   python app.py
   ```

7. **Access the Portal**
   Open your browser and navigate to: `http://127.0.0.1:5000`

### First Time Setup
After seeding, you can log in with these demo accounts:

## 🔑 Demo Accounts

| Role | Email | Password | Owner/Name | Description |
|------|-------|----------|------------|-------------|
| 👨‍💼 Job Seeker | alex.thompson@email.com | seeker123 | Alex Thompson | Browse and apply to jobs |
| 🏢 Recruiter | recruiter@google.com | recruiter123 | Google Recruiter | Post jobs and review applications |
| 🔐 Admin | admin@jobportal.com | admin123 | Sadhna | Full platform access |

Additional demo accounts are available for other companies (Microsoft, Amazon, Meta, etc.)

⚠️ **Security Note**: Change all default passwords in production!

## Project Structure

```
job portal web/
├── app.py                 # Main Flask application
├── instance/
│   └── jobportal.db      # SQLite database
├── static/
│   └── css/
│       ├── styles.css    # Source CSS with Tailwind directives
│       └── output.css    # Compiled CSS
├── templates/            # Jinja2 templates
│   ├── base.html        # Base template
│   ├── index.html       # Landing page
│   ├── jobs.html        # Job listings
│   ├── job_detail.html  # Job details
│   ├── apply_job.html   # Application form
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   └── [dashboard templates]
├── package.json         # Node dependencies
├── postcss.config.js    # PostCSS configuration
└── README.md           # This file
```

## Database Models

### User
- Stores user information (job seekers, recruiters, admins)
- Handles authentication with password hashing

### Job
- Job postings with details like title, company, location, salary
- Links to recruiter who posted the job

### Application
- Job applications with cover letters and resumes
- Tracks application status

### SavedJob
- Allows job seekers to save jobs for later viewing

## Available Routes

### Public Routes
- `/` - Landing page
- `/jobs` - Browse all jobs with filters
- `/job/<id>` - View job details
- `/login` - User login
- `/register` - User registration

### Job Seeker Routes (requires authentication)
- `/dashboard` - Job seeker dashboard
- `/job/<id>/apply` - Apply to a job
- `/my-applications` - View all applications
- `/saved-jobs` - View saved jobs
- `/job/<id>/save` - Save/unsave a job (API endpoint)

### Recruiter Routes (requires authentication)
- `/recruiter/dashboard` - Recruiter dashboard
- `/recruiter/job/new` - Post a new job
- `/recruiter/job/<id>/edit` - Edit job posting
- `/recruiter/job/<id>/delete` - Delete job posting
- `/recruiter/job/<id>/applications` - View applications for a job
- `/recruiter/application/<id>/update` - Update application status

### Admin Routes (requires authentication)
- `/admin/dashboard` - Admin dashboard with statistics
- `/admin/users` - View all users
- `/admin/jobs` - View all jobs

## 💻 Development

### Live CSS Development
Watch for CSS changes and auto-rebuild:
```bash
npm run watch:css
```

### Database Management

**Initialize/Reset Database:**
```bash
# Delete existing database
rm instance/jobportal.db

# Run application (auto-creates database)
python run.py

# Seed with sample data
python seed_data.py
```

### Environment Variables
Create a `.env` file (see `.env.example`):
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///jobportal.db
DEBUG=True
```

### Code Structure Best Practices
- Models are defined in `app.py`
- Templates use Jinja2 with inheritance from `base.html`
- CSS follows BEM-like methodology with custom properties
- All styling uses Tailwind v4 + custom CSS components

## Security Notes

- Passwords are hashed using Werkzeug's security module
- Flask-Login manages user sessions
- Secret key should be changed in production
- CSRF protection can be added using Flask-WTF

## 📦 Deployment

### Production Checklist
- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False` in production
- [ ] Change all default passwords
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Set up HTTPS/SSL
- [ ] Configure email server for notifications
- [ ] Set up backups for database
- [ ] Add rate limiting
- [ ] Implement CSRF protection
- [ ] Configure proper logging

### Recommended Production Stack
- **Web Server**: Gunicorn or uWSGI
- **Reverse Proxy**: Nginx
- **Database**: PostgreSQL
- **Hosting**: Heroku, AWS, DigitalOcean, or Render
- **File Storage**: AWS S3 for resume uploads

### Example Production Setup (Linux)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🎨 Customization

### Branding
- Update logo in `templates/base.html`
- Modify colors in `static/css/styles.css` (`:root` variables)
- Change company name throughout templates

### Styling
All design tokens are in CSS variables:
```css
--color-primary: #1560BD;
--color-success: #10B981;
--color-error: #EF4444;
```

### Features
Enable/disable features by modifying routes in `app.py`

## 🔧 Troubleshooting

**Issue**: CSS not loading
```bash
npm run build:css
```

**Issue**: Database locked
```bash
# Stop all Python processes
# Delete jobportal.db
# Restart application
```

**Issue**: Icons not showing
- Check Lucide CSS is loading
- Clear browser cache

## 📊 Sample Data Statistics

The seed script creates:
- **10 Recruiters** from companies like Google, Microsoft, Amazon
- **12 Job Seekers** with realistic profiles
- **70+ Job Postings** across multiple categories:
  - Software Development (Frontend, Backend, Full-Stack, DevOps)
  - Data Science & AI (ML Engineers, Data Scientists)
  - Product & Design (PMs, UX Designers)
  - Marketing & Sales
- **50+ Applications** with various statuses
- **30+ Saved Jobs** across different users

## 🌟 Advanced Features

### Search & Filtering
- Full-text search across job titles, descriptions, companies
- Multiple filter combinations (job type, experience, location)
- Pagination for large result sets

### Application Management
- Status tracking (Pending → Reviewed → Accepted/Rejected)
- Cover letter management
- Resume file uploads (PDF, DOC, DOCX)
- Application history with timestamps

### User Experience
- Responsive design (mobile, tablet, desktop)
- Flash messages with auto-dismiss
- Loading indicators
- Smooth animations and transitions
- Empty states with helpful CTAs

## 🛡️ Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- SQL injection protection via SQLAlchemy ORM
- XSS protection through template escaping
- File upload validation
- Remember me functionality

## 📈 Future Enhancements

### Planned Features
- 📧 Email notifications for application updates
- 🔍 Advanced search with salary range sliders
- 🏢 Company profile pages with reviews
- 📄 AI-powered resume parsing
- 📊 Application analytics and insights
- ✉️ Email verification for new users
- 🔑 Password reset via email
- 🔐 Two-factor authentication
- 💬 In-app messaging between recruiters and candidates
- ⭐ Job rating and review system
- 🤖 AI job recommendations
- 📱 Mobile app (React Native)

### API Development
Future REST API endpoints for mobile apps and integrations

## 🤝 Contributing

This is an educational project. Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues, questions, or suggestions:
- Open an issue in the repository
- Review existing documentation
- Check troubleshooting section

## 🎓 Learning Resources

This project demonstrates:
- Flask web framework
- SQLAlchemy ORM
- User authentication with Flask-Login
- Tailwind CSS v4
- Jinja2 templating
- Form validation
- File uploads
- Pagination
- Database relationships

## License

This project is for educational purposes.

## Support

For issues or questions, please create an issue in the repository.
