#!/usr/bin/env python
"""
Database initialization script
Run this to set up the database with initial data
"""

import os
import sys
from app import create_app, db
from models import User, Course, Enrollment, ContactMessage, Testimonial, Statistic
from routes.courses import INITIAL_COURSES

def init_db():
    """Initialize database with tables and sample data"""
    
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    with app.app_context():
        print("🔄 Initializing database...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if courses exist
        if Course.query.count() == 0:
            print("📚 Adding courses...")
            for course_data in INITIAL_COURSES:
                course = Course(**course_data)
                db.session.add(course)
            db.session.commit()
            print(f"✅ Added {len(INITIAL_COURSES)} courses")
        else:
            print("ℹ️  Courses already exist")
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@sec2systems.com').first()
        if not admin:
            print("👤 Creating admin user...")
            admin = User(
                name='Admin User',
                email='admin@sec2systems.com',
                is_admin=True,
                experience_level='advanced'
            )
            admin.set_password('admin@123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")
            print("   Email: admin@sec2systems.com")
            print("   Password: admin@123")
            print("   ⚠️  Change this password in production!")
        else:
            print("ℹ️  Admin user already exists")
        
        # Create sample users
        if User.query.filter_by(is_admin=False).count() == 0:
            print("👥 Creating sample users...")
            sample_users = [
                {
                    'name': 'Rajesh Kumar',
                    'email': 'rajesh@example.com',
                    'password': 'password123',
                    'phone': '9876543210',
                    'experience_level': 'beginner'
                },
                {
                    'name': 'Priya Singh',
                    'email': 'priya@example.com',
                    'password': 'password123',
                    'phone': '9876543211',
                    'experience_level': 'intermediate'
                },
                {
                    'name': 'Amit Kapoor',
                    'email': 'amit@example.com',
                    'password': 'password123',
                    'phone': '9876543212',
                    'experience_level': 'advanced'
                }
            ]
            
            for user_data in sample_users:
                password = user_data.pop('password')
                user = User(**user_data)
                user.set_password(password)
                db.session.add(user)
            
            db.session.commit()
            print(f"✅ Created {len(sample_users)} sample users")
        else:
            print("ℹ️  Sample users already exist")
        
        # Create sample testimonials
        if Testimonial.query.count() == 0:
            print("⭐ Creating sample testimonials...")
            testimonials = [
                {
                    'name': 'Rajesh Kumar',
                    'title': 'AI Engineer at TechCorp',
                    'content': 'SEC2SYSTEMS transformed my career. The hands-on training and industry mentorship helped me land my dream job in 3 months!',
                    'rating': 5,
                    'is_approved': True
                },
                {
                    'name': 'Priya Singh',
                    'title': 'Data Scientist at CloudTech',
                    'content': 'The best investment I made in myself. The trainers are industry experts and the curriculum is always updated with latest trends.',
                    'rating': 5,
                    'is_approved': True
                },
                {
                    'name': 'Amit Kapoor',
                    'title': 'DevOps Engineer at CloudStack',
                    'content': 'No upfront payment and guaranteed job placement made all the difference. Now I\'m earning more than I ever expected!',
                    'rating': 5,
                    'is_approved': True
                }
            ]
            
            for testimonial_data in testimonials:
                testimonial = Testimonial(**testimonial_data)
                db.session.add(testimonial)
            
            db.session.commit()
            print(f"✅ Created {len(testimonials)} sample testimonials")
        else:
            print("ℹ️  Testimonials already exist")
        
        # Create sample statistics
        if Statistic.query.count() == 0:
            print("📊 Creating statistics...")
            stats = [
                {'key': 'students_trained', 'value': '5000', 'description': 'Total students trained'},
                {'key': 'placement_rate', 'value': '95', 'description': 'Placement success rate (%)'},
                {'key': 'industry_partners', 'value': '50', 'description': 'Industry partnerships'},
                {'key': 'courses_available', 'value': '13', 'description': 'Active courses'}
            ]
            
            for stat_data in stats:
                stat = Statistic(**stat_data)
                db.session.add(stat)
            
            db.session.commit()
            print(f"✅ Created {len(stats)} statistics")
        else:
            print("ℹ️  Statistics already exist")
        
        print("\n✨ Database initialization complete!")
        print("\n📊 Database Summary:")
        print(f"   Users: {User.query.count()}")
        print(f"   Courses: {Course.query.count()}")
        print(f"   Enrollments: {Enrollment.query.count()}")
        print(f"   Testimonials: {Testimonial.query.count()}")
        print(f"   Contact Messages: {ContactMessage.query.count()}")
        print(f"   Statistics: {Statistic.query.count()}")

def reset_db():
    """Reset database (dangerous - deletes all data)"""
    
    response = input("⚠️  WARNING: This will delete all data! Are you sure? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    with app.app_context():
        print("🗑️  Dropping all tables...")
        db.drop_all()
        print("✅ All tables dropped")
        
        print("🔄 Recreating tables...")
        init_db()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_db()
    else:
        init_db()
