from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobportal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'job_seeker', 'recruiter', 'admin'
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    job_type = db.Column(db.String(50))  # 'full-time', 'part-time', 'contract'
    experience = db.Column(db.String(50))
    salary = db.Column(db.String(100))
    skills = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # 'active', 'closed'
    recruiter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('saved_jobs', lazy=True, cascade='all, delete-orphan'))
    job = db.relationship('Job', backref=db.backref('saved_by', lazy=True, cascade='all, delete-orphan'))
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'job_id', name='unique_user_job'),
    )

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    resume_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, accepted, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Set up relationships after all models are defined
User.jobs_posted = db.relationship('Job', backref='recruiter', lazy=True, foreign_keys='Job.recruiter_id')
User.applications = db.relationship('Application', backref='applicant', lazy=True)

Job.applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    recent_jobs = Job.query.filter_by(status='active').order_by(Job.created_at.desc()).limit(6).all()
    return render_template('index.html', recent_jobs=recent_jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Please provide email and password', 'error')
        else:
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                flash(f'Welcome back, {user.full_name or user.username}!', 'success')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        role = request.form.get('role')
        
        # Validation
        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if not full_name:
            errors.append('Full name is required')
        if not role or role not in ['job_seeker', 'recruiter']:
            errors.append('Please select a valid role')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
        else:
            user = User(username=username, email=email, full_name=full_name, phone=phone, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'recruiter':
        return redirect(url_for('recruiter_dashboard'))
    else:
        return redirect(url_for('job_seeker_dashboard'))

@app.route('/job-seeker/dashboard')
@login_required
def job_seeker_dashboard():
    if current_user.role != 'job_seeker':
        return redirect(url_for('dashboard'))
    
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template('job_seeker_dashboard.html', applications=applications)

@app.route('/recruiter/dashboard')
@login_required
def recruiter_dashboard():
    if current_user.role != 'recruiter':
        return redirect(url_for('dashboard'))
    
    jobs = Job.query.filter_by(recruiter_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template('recruiter_dashboard.html', jobs=jobs)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    active_jobs = Job.query.filter_by(status='active').count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_jobs=total_jobs,
                         total_applications=total_applications,
                         active_jobs=active_jobs,
                         recent_users=recent_users,
                         recent_jobs=recent_jobs)

@app.route('/jobs')
def jobs():
    # Get search parameters
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('type', '')
    experience = request.args.get('experience', '')
    min_salary = request.args.get('min_salary', type=int)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Start with base query
    query = Job.query.filter_by(status='active')
    
    # Apply filters
    if search:
        query = query.filter(
            (Job.title.ilike(f'%{search}%')) |
            (Job.skills.ilike(f'%{search}%')) |
            (Job.description.ilike(f'%{search}%')) |
            (Job.company.ilike(f'%{search}%'))
        )
    
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
        
    if job_type and job_type != 'all':
        query = query.filter(Job.job_type == job_type)
        
    if experience and experience != 'all':
        query = query.filter(Job.experience == experience)
        
    if min_salary:
        query = query.filter(Job.salary.isnot(None))
    
    # Get the filtered jobs with pagination
    jobs_pagination = query.order_by(Job.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # Extract jobs from pagination
    jobs = jobs_pagination.items
    
    # Get unique values for filters
    job_types = db.session.query(Job.job_type).distinct().all()
    job_types = [t[0] for t in job_types if t[0]]  # Extract from tuple and filter out None
    
    experience_levels = db.session.query(Job.experience).distinct().all()
    experience_levels = [e[0] for e in experience_levels if e[0]]  # Extract from tuple and filter out None
    
    # Check which jobs are saved by the current user
    saved_job_ids = []
    if current_user.is_authenticated:
        saved_job_ids = [sj.job_id for sj in current_user.saved_jobs]
    
    return render_template(
        'jobs.html',
        jobs=jobs,
        jobs_pagination=jobs_pagination,
        search=search,
        location=location,
        job_types=job_types,
        experience_levels=experience_levels,
        selected_type=job_type,
        selected_experience=experience,
        selected_min_salary=min_salary,
        saved_job_ids=saved_job_ids
    )

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    has_applied = False
    is_saved = False
    
    if current_user.is_authenticated:
        has_applied = Application.query.filter_by(job_id=job_id, user_id=current_user.id).first() is not None
        is_saved = SavedJob.query.filter_by(job_id=job_id, user_id=current_user.id).first() is not None
    
    # Get similar jobs (same company or similar title)
    similar_jobs = Job.query.filter(
        Job.id != job_id,
        Job.status == 'active',
        (Job.company == job.company) | (Job.title.ilike(f'%{job.title.split()[0]}%'))
    ).limit(3).all()
    
    return render_template('job_detail.html', job=job, has_applied=has_applied, is_saved=is_saved, similar_jobs=similar_jobs)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}

@app.route('/job/<int:job_id>/apply', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check if user has already applied
    existing_application = Application.query.filter_by(job_id=job_id, user_id=current_user.id).first()
    if existing_application:
        flash('You have already applied to this job', 'warning')
        return redirect(url_for('job_detail', job_id=job_id))
        
    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter', '').strip()
        resume = request.files.get('resume')
        
        if not cover_letter:
            flash('Cover letter is required', 'danger')
            return redirect(request.url)
            
        # Handle resume upload
        resume_url = None
        if resume and resume.filename != '':
            if not allowed_file(resume.filename):
                flash('Invalid file type. Only PDF, DOC, and DOCX files are allowed.', 'danger')
                return redirect(request.url)
                
            # Create uploads directory if it doesn't exist
            if not os.path.exists('uploads/resumes'):
                os.makedirs('uploads/resumes')
                
            # Generate a unique filename
            filename = secure_filename(f"{current_user.id}_{int(datetime.utcnow().timestamp())}_{resume.filename}")
            resume_path = os.path.join('uploads/resumes', filename)
            resume.save(resume_path)
            resume_url = resume_path
            
        # Create application
        application = Application(
            job_id=job_id,
            user_id=current_user.id,
            cover_letter=cover_letter,
            resume_url=resume_url,
            status='pending'
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Your application has been submitted successfully!', 'success')
        return redirect(url_for('my_applications'))
    
    return render_template('apply_job.html', job=job)

@app.route('/job/<int:job_id>/save', methods=['POST'])
@login_required
def save_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check if job is already saved
    saved_job = SavedJob.query.filter_by(
        user_id=current_user.id,
        job_id=job_id
    ).first()
    
    if saved_job:
        db.session.delete(saved_job)
        db.session.commit()
        return jsonify({'saved': False, 'message': 'Job removed from saved jobs'}), 200
    else:
        new_saved = SavedJob(user_id=current_user.id, job_id=job_id)
        db.session.add(new_saved)
        db.session.commit()
        return jsonify({'saved': True, 'message': 'Job saved successfully'}), 200

@app.route('/my-applications')
@login_required
def my_applications():
    if current_user.role != 'job_seeker':
        flash('Only job seekers can view applications', 'error')
        return redirect(url_for('dashboard'))
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get filter parameters
    status = request.args.get('status', 'all')
    
    # Base query
    query = Application.query.filter_by(user_id=current_user.id)
    
    # Apply status filter
    if status and status != 'all':
        query = query.filter_by(status=status)
    
    # Order by application date (newest first)
    applications = query.order_by(Application.applied_at.desc())
    
    # Paginate results
    applications_pagination = applications.paginate(page=page, per_page=per_page, error_out=False)
    
    # Get application status counts for the filter
    status_counts = {
        'all': Application.query.filter_by(user_id=current_user.id).count(),
        'pending': Application.query.filter_by(user_id=current_user.id, status='pending').count(),
        'reviewed': Application.query.filter_by(user_id=current_user.id, status='reviewed').count(),
        'accepted': Application.query.filter_by(user_id=current_user.id, status='accepted').count(),
        'rejected': Application.query.filter_by(user_id=current_user.id, status='rejected').count()
    }
    
    return render_template(
        'my_applications.html',
        applications_pagination=applications_pagination,
        status_counts=status_counts,
        current_status=status
    )

@app.route('/saved-jobs')
@login_required
def saved_jobs():
    if current_user.role != 'job_seeker':
        flash('Only job seekers can save jobs', 'error')
        return redirect(url_for('dashboard'))
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get saved jobs with job details
    query = SavedJob.query.filter_by(user_id=current_user.id).join(Job).filter(Job.status == 'active').order_by(SavedJob.saved_at.desc())
    
    # Paginate results
    saved_jobs_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('saved_jobs.html', saved_jobs_pagination=saved_jobs_pagination)

@app.route('/recruiter/job/new', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'recruiter':
        flash('Only recruiters can post jobs', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        job = Job(
            title=request.form.get('title'),
            company=request.form.get('company'),
            location=request.form.get('location'),
            job_type=request.form.get('job_type'),
            experience=request.form.get('experience'),
            salary=request.form.get('salary'),
            skills=request.form.get('skills'),
            description=request.form.get('description'),
            requirements=request.form.get('requirements'),
            recruiter_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('recruiter_dashboard'))
    
    return render_template('post_job.html')

@app.route('/recruiter/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if current_user.role != 'recruiter' or job.recruiter_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.company = request.form.get('company')
        job.location = request.form.get('location')
        job.job_type = request.form.get('job_type')
        job.experience = request.form.get('experience')
        job.salary = request.form.get('salary')
        job.skills = request.form.get('skills')
        job.description = request.form.get('description')
        job.requirements = request.form.get('requirements')
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('recruiter_dashboard'))
    
    return render_template('edit_job.html', job=job)

@app.route('/recruiter/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if current_user.role != 'recruiter' or job.recruiter_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('recruiter_dashboard'))

@app.route('/recruiter/job/<int:job_id>/applications')
@login_required
def view_applications(job_id):
    job = Job.query.get_or_404(job_id)
    
    if current_user.role != 'recruiter' or job.recruiter_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    applications = Application.query.filter_by(job_id=job_id).order_by(Application.applied_at.desc()).all()
    return render_template('view_applications.html', job=job, applications=applications)

@app.route('/recruiter/application/<int:application_id>/update', methods=['POST'])
@login_required
def update_application_status(application_id):
    application = Application.query.get_or_404(application_id)
    
    if current_user.role != 'recruiter' or application.job.recruiter_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    new_status = request.form.get('status')
    application.status = new_status
    db.session.commit()
    flash('Application status updated!', 'success')
    return redirect(url_for('view_applications', job_id=application.job_id))

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/jobs')
@login_required
def admin_jobs():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin_jobs.html', jobs=jobs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@jobportal.com', role='admin', full_name='Sadhna')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True)