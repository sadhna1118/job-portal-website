# 🤝 Contributing to Job Portal

Thank you for your interest in contributing to Job Portal! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all.

### Our Standards
- ✅ Be respectful and inclusive
- ✅ Welcome newcomers and help them learn
- ✅ Focus on what is best for the community
- ✅ Show empathy towards others

- ❌ No harassment, trolling, or insulting comments
- ❌ No political or religious discussions
- ❌ No spam or self-promotion

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git
- Text editor (VS Code recommended)

### Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/job-portal.git
cd job-portal

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/job-portal.git
```

## 💻 Development Setup

### 1. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node dependencies
npm install
```

### 3. Set Up Database
```bash
# Initialize database
python run.py

# Seed sample data
python seed_data.py
```

### 4. Run Development Server
```bash
# Terminal 1: Watch CSS
npm run watch:css

# Terminal 2: Run Flask
python app.py
```

## 🔨 Making Changes

### 1. Create a Branch
```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes
- Write clear, concise commit messages
- Keep commits focused and atomic
- Test your changes thoroughly

### 3. Commit Guidelines
```bash
# Good commit messages
git commit -m "Add job search filtering by salary range"
git commit -m "Fix application status update bug"
git commit -m "Improve mobile responsive design for job cards"

# Bad commit messages
git commit -m "Fixed stuff"
git commit -m "WIP"
git commit -m "asdf"
```

## 📐 Coding Standards

### Python Style (PEP 8)
```python
# Good
def get_active_jobs(limit=10):
    """Fetch active jobs from database."""
    return Job.query.filter_by(status='active').limit(limit).all()

# Bad
def getActiveJobs(limit = 10):
    return Job.query.filter_by(status = 'active').limit(limit).all()
```

### HTML/Jinja2 Templates
```html
<!-- Good: Consistent indentation -->
<div class="job-card">
    <h3 class="job-title">{{ job.title }}</h3>
    <p class="job-company">{{ job.company }}</p>
</div>

<!-- Bad: Inconsistent formatting -->
<div class="job-card"><h3 class="job-title">{{ job.title }}</h3>
<p class="job-company">{{ job.company }}</p></div>
```

### CSS/Tailwind
```css
/* Good: Organized, commented */
/* Job Cards */
.job-card {
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
}

/* Bad: Unorganized, no comments */
.job-card{background:#fff;border:1px solid #eee;padding:20px;}
```

### JavaScript
```javascript
// Good: Clear, documented
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Bad: Unclear, no validation
function v(e){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)}
```

## 🧪 Testing

### Manual Testing Checklist
Before submitting, test:
- [ ] All forms work correctly
- [ ] Error messages display properly
- [ ] Navigation works on all pages
- [ ] Responsive design on mobile/tablet
- [ ] Database operations complete successfully
- [ ] File uploads work (if applicable)

### Browser Testing
Test on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

### Test User Roles
Test features for:
- Job Seekers
- Recruiters
- Administrators
- Unauthenticated users

## 📝 Pull Request Process

### 1. Update Your Branch
```bash
# Get latest changes
git fetch upstream
git rebase upstream/main

# Resolve conflicts if any
git add .
git rebase --continue
```

### 2. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- Tested manually on Chrome, Firefox
- Added/updated tests
- All existing tests pass

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed my own code
- [ ] Commented complex code sections
- [ ] Updated documentation
- [ ] No new warnings generated
- [ ] Added tests that prove fix/feature works
```

### 4. Code Review
- Respond to feedback promptly
- Make requested changes
- Keep discussion focused and professional

### 5. Merge
Once approved, maintainers will merge your PR!

## 🐛 Reporting Bugs

### Before Reporting
- Check existing issues
- Try latest version
- Gather relevant information

### Bug Report Template
```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
Add screenshots if applicable

**Environment:**
- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Python version: [e.g., 3.11]

**Additional context**
Any other relevant information
```

## ✨ Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the feature

**Problem it Solves**
What problem does this solve?

**Proposed Solution**
Your proposed implementation

**Alternatives Considered**
Other approaches you thought of

**Additional Context**
Mockups, examples, etc.
```

## 💡 Development Tips

### Useful Commands
```bash
# Check Python code style
flake8 app.py

# Format Python code
black app.py

# Check for security issues
bandit -r app.py

# Profile database queries
FLASK_DEBUG=True python app.py
```

### Debug Mode
```python
# Enable detailed error messages
app.config['DEBUG'] = True

# SQL query logging
app.config['SQLALCHEMY_ECHO'] = True
```

### Common Patterns

**Adding a New Route:**
```python
@app.route('/new-feature')
@login_required
def new_feature():
    # Implementation
    return render_template('new_feature.html')
```

**Adding a New Model:**
```python
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Adding a New Template:**
```html
{% extends "base.html" %}

{% block title %}New Feature{% endblock %}

{% block content %}
<!-- Your content -->
{% endblock %}
```

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

## 🎯 Good First Issues

Look for issues labeled `good first issue` - these are great for newcomers!

## 📞 Questions?

- Open a discussion on GitHub
- Check existing documentation
- Ask in the community forum

---

**Thank you for contributing! 🎉**