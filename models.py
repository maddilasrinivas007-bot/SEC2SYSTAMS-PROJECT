from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    experience_level = db.Column(db.String(50), default='beginner')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'experience_level': self.experience_level,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'enrollments_count': len(self.enrollments)
        }

class Course(db.Model):
    """Course model"""
    __tablename__ = 'courses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)  # ai, data, cloud
    icon = db.Column(db.String(50), default='fas fa-graduation-cap')
    duration = db.Column(db.String(50), default='8 weeks')
    level = db.Column(db.String(50), default='Beginner')
    instructor = db.Column(db.String(120), nullable=True)
    max_students = db.Column(db.Integer, default=30)
    price = db.Column(db.Float, default=0.0)  # Free courses by default
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'duration': self.duration,
            'level': self.level,
            'instructor': self.instructor,
            'max_students': self.max_students,
            'price': self.price,
            'is_active': self.is_active,
            'enrolled_count': len(self.enrollments),
            'created_at': self.created_at.isoformat()
        }

class Enrollment(db.Model):
    """Enrollment model - tracks student enrollments"""
    __tablename__ = 'enrollments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False, index=True)
    status = db.Column(db.String(50), default='active')  # active, completed, paused
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)
    progress = db.Column(db.Float, default=0.0)  # 0-100%
    certificate_issued = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_user_course'),)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'course': self.course.to_dict(),
            'status': self.status,
            'progress': self.progress,
            'certificate_issued': self.certificate_issued,
            'enrollment_date': self.enrollment_date.isoformat(),
            'completion_date': self.completion_date.isoformat() if self.completion_date else None
        }

class ContactMessage(db.Model):
    """Contact form messages"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_replied = db.Column(db.Boolean, default=False)
    reply_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'phone': self.phone,
            'is_replied': self.is_replied,
            'reply_message': self.reply_message,
            'created_at': self.created_at.isoformat()
        }

class Testimonial(db.Model):
    """Student testimonials"""
    __tablename__ = 'testimonials'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)  # 1-5 stars
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'content': self.content,
            'rating': self.rating,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat()
        }

class Statistic(db.Model):
    """Application statistics"""
    __tablename__ = 'statistics'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'key': self.key,
            'value': self.value,
            'description': self.description
        }
