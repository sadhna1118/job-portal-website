"""
Production-ready run script for Job Portal
"""
import os
from app import app, db, User

def init_db():
    """Initialize database and create admin user if needed"""
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@jobportal.com',
                role='admin',
                full_name='Admin User',
                phone='+1-555-000-0000'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: admin@jobportal.com / admin123")
        else:
            print("✅ Admin user already exists")

if __name__ == '__main__':
    print("🚀 Starting Job Portal...")
    
    # Initialize database
    init_db()
    
    # Get configuration from environment
    debug_mode = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"🌐 Server running on http://{host}:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )