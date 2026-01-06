"""
Seed script to populate the database with realistic sample data
"""
from app import app, db, User, Job, Application, SavedJob
from datetime import datetime, timedelta
import random

# Sample data for realistic job portal
COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Tesla",
    "Salesforce", "Adobe", "Oracle", "IBM", "Intel", "Uber", "Airbnb",
    "Spotify", "Twitter", "LinkedIn", "Shopify", "Stripe", "Slack"
]

JOB_TITLES = {
    "Software Development": [
        "Senior Software Engineer", "Full Stack Developer", "Backend Developer",
        "Frontend Developer", "DevOps Engineer", "Site Reliability Engineer",
        "Mobile Developer (iOS)", "Mobile Developer (Android)", "Software Architect"
    ],
    "Data & AI": [
        "Data Scientist", "Machine Learning Engineer", "Data Engineer",
        "AI Research Scientist", "Data Analyst", "Business Intelligence Analyst"
    ],
    "Product & Design": [
        "Product Manager", "Senior Product Designer", "UX/UI Designer",
        "Product Owner", "UX Researcher", "Graphic Designer"
    ],
    "Marketing & Sales": [
        "Digital Marketing Manager", "Content Marketing Manager", "Sales Executive",
        "Marketing Analyst", "SEO Specialist", "Social Media Manager"
    ],
    "Other": [
        "Project Manager", "Scrum Master", "Technical Writer",
        "Quality Assurance Engineer", "Security Engineer", "Cloud Architect"
    ]
}

LOCATIONS = [
    "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
    "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Denver, CO",
    "Remote", "Hybrid - Bay Area", "Remote (US)", "Atlanta, GA"
]

JOB_TYPES = ["full-time", "part-time", "contract", "internship"]

EXPERIENCE_LEVELS = ["Entry Level", "1-3 years", "3-5 years", "5-10 years", "10+ years"]

SKILLS_BY_CATEGORY = {
    "Software Development": [
        "Python, Django, Flask, PostgreSQL",
        "JavaScript, React, Node.js, MongoDB",
        "Java, Spring Boot, Microservices, AWS",
        "TypeScript, Angular, Vue.js, REST APIs",
        "C++, System Design, Linux, Docker",
        "Go, Kubernetes, CI/CD, Terraform",
        "Swift, iOS, UIKit, SwiftUI",
        "Kotlin, Android, Jetpack Compose",
        "Ruby, Rails, Redis, GraphQL"
    ],
    "Data & AI": [
        "Python, TensorFlow, PyTorch, SQL",
        "Machine Learning, Deep Learning, NLP",
        "Apache Spark, Hadoop, Kafka, Airflow",
        "SQL, Python, Tableau, Power BI",
        "Statistics, R, Python, Data Visualization"
    ],
    "Product & Design": [
        "Product Strategy, User Research, Analytics",
        "Figma, Sketch, Adobe XD, Prototyping",
        "UX Research, User Testing, Wireframing",
        "Agile, Scrum, JIRA, Roadmapping"
    ],
    "Marketing & Sales": [
        "SEO, SEM, Google Analytics, Content Strategy",
        "HubSpot, Salesforce, Email Marketing",
        "Social Media Marketing, Content Creation",
        "B2B Sales, CRM, Lead Generation"
    ],
    "Other": [
        "Agile, Scrum, JIRA, Confluence",
        "Test Automation, Selenium, Performance Testing",
        "Penetration Testing, Security Audits, CISSP",
        "AWS, Azure, GCP, Terraform, Kubernetes"
    ]
}

JOB_DESCRIPTIONS = {
    "Software Engineer": """We're looking for a talented software engineer to join our growing team. You'll work on cutting-edge technology, collaborate with cross-functional teams, and help build products used by millions.

Responsibilities:
• Design, develop, and maintain scalable applications
• Write clean, maintainable, and well-tested code
• Participate in code reviews and technical discussions
• Collaborate with product managers and designers
• Troubleshoot and debug production issues
• Mentor junior engineers and contribute to team growth

What We Offer:
• Competitive salary and equity package
• Comprehensive health, dental, and vision insurance
• 401(k) matching and retirement benefits
• Flexible work arrangements
• Professional development budget
• Collaborative and inclusive culture""",
    
    "Data Scientist": """Join our data science team to solve complex business problems using advanced analytics and machine learning. You'll work with large datasets and cutting-edge tools to drive data-driven decision making.

Responsibilities:
• Develop predictive models and machine learning algorithms
• Analyze large datasets to extract actionable insights
• Build data pipelines and automation workflows
• Present findings to stakeholders and leadership
• Collaborate with engineering teams on model deployment
• Stay current with latest ML/AI research and techniques

What We Offer:
• Competitive compensation package
• State-of-the-art tools and infrastructure
• Conference attendance and learning opportunities
• Flexible working hours
• Strong emphasis on work-life balance
• Collaborative research environment""",

    "Product Manager": """We're seeking an experienced product manager to drive the strategy and execution of our product roadmap. You'll work closely with engineering, design, and business teams to deliver exceptional user experiences.

Responsibilities:
• Define product vision and strategy
• Conduct user research and market analysis
• Prioritize features and manage product backlog
• Work with engineering teams on technical requirements
• Track and analyze product metrics
• Communicate product updates to stakeholders

What We Offer:
• Competitive salary and benefits
• Impact-driven work environment
• Career growth opportunities
• Flexible work schedule
• Modern office spaces
• Company-sponsored events and activities""",

    "Designer": """We're looking for a creative designer who can craft beautiful, intuitive user experiences. You'll work on diverse projects and collaborate with talented teams to bring ideas to life.

Responsibilities:
• Create user-centered designs for web and mobile
• Develop wireframes, prototypes, and high-fidelity mockups
• Conduct user research and usability testing
• Maintain and evolve design system
• Collaborate with product and engineering teams
• Present design concepts and rationale

What We Offer:
• Competitive compensation
• Latest design tools and software
• Creative freedom and autonomy
• Supportive design community
• Professional development opportunities
• Flexible work environment"""
}

REQUIREMENTS = {
    "Entry Level": """Requirements:
• Bachelor's degree in relevant field or equivalent experience
• Strong problem-solving and analytical skills
• Excellent communication abilities
• Eagerness to learn and grow
• Team player with collaborative mindset
• Portfolio or projects demonstrating skills (preferred)""",
    
    "Mid Level": """Requirements:
• 3+ years of professional experience in relevant field
• Strong technical skills and domain knowledge
• Proven track record of successful projects
• Experience working in agile environments
• Excellent problem-solving abilities
• Strong communication and collaboration skills
• Bachelor's degree or equivalent experience""",
    
    "Senior Level": """Requirements:
• 5+ years of professional experience
• Deep expertise in relevant technologies/domain
• Experience leading projects and mentoring teams
• Strong system design and architecture skills
• Excellent communication and leadership abilities
• Track record of delivering complex projects
• Bachelor's or Master's degree in relevant field"""
}

def generate_salary(level):
    """Generate realistic salary based on experience level"""
    if "Entry" in level:
        return f"${random.randint(60, 90)}K - ${random.randint(90, 120)}K"
    elif "1-3" in level:
        return f"${random.randint(80, 110)}K - ${random.randint(110, 140)}K"
    elif "3-5" in level:
        return f"${random.randint(100, 130)}K - ${random.randint(130, 170)}K"
    elif "5-10" in level:
        return f"${random.randint(130, 170)}K - ${random.randint(170, 220)}K"
    else:
        return f"${random.randint(160, 200)}K - ${random.randint(200, 300)}K"

def get_description_template(title):
    """Get appropriate description template based on job title"""
    title_lower = title.lower()
    if any(word in title_lower for word in ['engineer', 'developer', 'devops']):
        return "Software Engineer"
    elif any(word in title_lower for word in ['data', 'scientist', 'analyst']):
        return "Data Scientist"
    elif any(word in title_lower for word in ['product', 'manager']):
        return "Product Manager"
    elif any(word in title_lower for word in ['designer', 'ux', 'ui']):
        return "Designer"
    else:
        return "Software Engineer"

def get_requirements_template(level):
    """Get appropriate requirements based on experience level"""
    if "Entry" in level or "1-3" in level:
        return REQUIREMENTS["Entry Level"]
    elif "3-5" in level:
        return REQUIREMENTS["Mid Level"]
    else:
        return REQUIREMENTS["Senior Level"]

def seed_database():
    """Populate database with sample data"""
    with app.app_context():
        # Create all tables first
        print("Creating database tables...")
        db.create_all()
        
        # Clear existing data (except admin)
        print("Clearing existing data...")
        try:
            Application.query.delete()
            SavedJob.query.delete()
            Job.query.delete()
            User.query.filter(User.username != 'admin').delete()
        except Exception as e:
            print(f"Note: {e}")
            db.session.rollback()
        
        print("Creating sample users...")
        
        # Create recruiters (one per company subset)
        recruiters = []
        for i, company in enumerate(COMPANIES[:10]):
            recruiter = User(
                username=f"recruiter_{company.lower().replace(' ', '_')}",
                email=f"recruiter@{company.lower().replace(' ', '')}.com",
                role='recruiter',
                full_name=f"{['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emily', 'Chris', 'Lisa', 'Tom', 'Anna'][i]} {['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'][i]}",
                phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            )
            recruiter.set_password('recruiter123')
            db.session.add(recruiter)
            recruiters.append(recruiter)
        
        # Create job seekers
        job_seekers = []
        seeker_names = [
            ("Alex", "Thompson"), ("Jordan", "Lee"), ("Taylor", "Anderson"),
            ("Morgan", "White"), ("Casey", "Harris"), ("Riley", "Martin"),
            ("Avery", "Garcia"), ("Quinn", "Martinez"), ("Drew", "Robinson"),
            ("Sam", "Clark"), ("Jamie", "Lewis"), ("Cameron", "Walker")
        ]
        
        for i, (first, last) in enumerate(seeker_names):
            seeker = User(
                username=f"{first.lower()}_{last.lower()}",
                email=f"{first.lower()}.{last.lower()}@email.com",
                role='job_seeker',
                full_name=f"{first} {last}",
                phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            )
            seeker.set_password('seeker123')
            db.session.add(seeker)
            job_seekers.append(seeker)
        
        db.session.commit()
        print(f"Created {len(recruiters)} recruiters and {len(job_seekers)} job seekers")
        
        # Create diverse job postings
        print("Creating job postings...")
        all_jobs = []
        job_id = 1
        
        for category, titles in JOB_TITLES.items():
            for title in titles:
                # Create 1-2 jobs per title
                num_jobs = random.randint(1, 2)
                for _ in range(num_jobs):
                    recruiter = random.choice(recruiters)
                    company = COMPANIES[recruiters.index(recruiter) % len(COMPANIES)]
                    location = random.choice(LOCATIONS)
                    job_type = random.choice(JOB_TYPES)
                    experience = random.choice(EXPERIENCE_LEVELS)
                    
                    # Get appropriate skills for category
                    skills_list = SKILLS_BY_CATEGORY.get(category, SKILLS_BY_CATEGORY["Other"])
                    skills = random.choice(skills_list)
                    
                    # Generate description and requirements
                    desc_template = get_description_template(title)
                    description = JOB_DESCRIPTIONS[desc_template]
                    requirements = get_requirements_template(experience)
                    
                    # Calculate days ago (random between 1-30 days)
                    days_ago = random.randint(1, 30)
                    created_date = datetime.utcnow() - timedelta(days=days_ago)
                    
                    job = Job(
                        title=title,
                        company=company,
                        location=location,
                        job_type=job_type,
                        experience=experience,
                        salary=generate_salary(experience),
                        skills=skills,
                        description=description,
                        requirements=requirements,
                        status='active',
                        recruiter_id=recruiter.id,
                        created_at=created_date
                    )
                    db.session.add(job)
                    all_jobs.append(job)
                    job_id += 1
        
        db.session.commit()
        print(f"Created {len(all_jobs)} job postings")
        
        # Create sample applications (some job seekers apply to random jobs)
        print("Creating sample applications...")
        applications_created = 0
        statuses = ['pending', 'reviewed', 'accepted', 'rejected']
        
        for seeker in job_seekers:
            # Each seeker applies to 2-5 random jobs
            num_applications = random.randint(2, 5)
            applied_jobs = random.sample(all_jobs, min(num_applications, len(all_jobs)))
            
            for job in applied_jobs:
                # Random days ago (1-25 days, ensuring it's after job posting)
                max_days = min(25, (datetime.utcnow() - job.created_at).days)
                if max_days > 0:
                    days_ago = random.randint(1, max_days)
                    applied_date = datetime.utcnow() - timedelta(days=days_ago)
                else:
                    applied_date = datetime.utcnow()
                
                status = random.choice(statuses)
                
                cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.title} position at {job.company}. With my background and skills, I believe I would be a valuable addition to your team.

I have experience working with similar technologies and am passionate about delivering high-quality solutions. I'm particularly excited about the opportunity to work at {job.company} because of your innovative approach and strong company culture.

I would welcome the opportunity to discuss how my skills and experience align with your team's needs. Thank you for considering my application.

Best regards,
{seeker.full_name}"""
                
                application = Application(
                    job_id=job.id,
                    user_id=seeker.id,
                    cover_letter=cover_letter,
                    status=status,
                    applied_at=applied_date,
                    updated_at=applied_date if status == 'pending' else applied_date + timedelta(days=random.randint(1, 5))
                )
                db.session.add(application)
                applications_created += 1
        
        db.session.commit()
        print(f"Created {applications_created} applications")
        
        # Create saved jobs (some job seekers save jobs)
        print("Creating saved jobs...")
        saved_count = 0
        
        for seeker in job_seekers:
            # Each seeker saves 1-4 random jobs
            num_saved = random.randint(1, 4)
            saved_jobs = random.sample(all_jobs, min(num_saved, len(all_jobs)))
            
            for job in saved_jobs:
                days_ago = random.randint(1, 20)
                saved_date = datetime.utcnow() - timedelta(days=days_ago)
                
                saved_job = SavedJob(
                    user_id=seeker.id,
                    job_id=job.id,
                    saved_at=saved_date
                )
                try:
                    db.session.add(saved_job)
                    saved_count += 1
                except:
                    db.session.rollback()
        
        db.session.commit()
        print(f"Created {saved_count} saved jobs")
        
        # Update admin user's full name to Sadhna
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            admin_user.full_name = 'Sadhna'
            db.session.commit()
            print("✅ Updated admin name to 'Sadhna'")
        
        print("\n✅ Database seeded successfully!")
        print(f"\nSample Login Credentials:")
        print(f"Admin (Sadhna): admin@jobportal.com / admin123")
        print(f"Recruiter: recruiter@google.com / recruiter123")
        print(f"Job Seeker: alex_thompson@email.com / seeker123")

if __name__ == '__main__':
    print("🌱 Starting database seeding...")
    seed_database()