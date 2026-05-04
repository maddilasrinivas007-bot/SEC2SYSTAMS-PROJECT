from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Course, Enrollment, ContactMessage, Statistic
from routes.courses import INITIAL_COURSES

admin_bp = Blueprint('admin', __name__)

def check_admin(user_id):
    """Check if user is admin"""
    user = User.query.get(user_id)
    return user and user.is_admin

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """Get admin dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        # Collect statistics
        stats = {
            'total_users': User.query.filter_by(is_admin=False).count(),
            'total_courses': Course.query.filter_by(is_active=True).count(),
            'total_enrollments': Enrollment.query.count(),
            'total_messages': ContactMessage.query.count(),
            'pending_messages': ContactMessage.query.filter_by(is_replied=False).count(),
            'active_enrollments': Enrollment.query.filter_by(status='active').count(),
            'completed_enrollments': Enrollment.query.filter_by(status='completed').count()
        }
        
        return jsonify({
            'dashboard': stats,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    """Create a new course"""
    try:
        user_id = get_jwt_identity()
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required = ['name', 'description', 'category']
        for field in required:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if course already exists
        if Course.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Course already exists'}), 409
        
        # Create course
        course = Course(
            name=data['name'],
            description=data['description'],
            category=data['category'],
            icon=data.get('icon', 'fas fa-graduation-cap'),
            duration=data.get('duration', '8 weeks'),
            level=data.get('level', 'Beginner'),
            instructor=data.get('instructor', 'Expert Instructor'),
            price=data.get('price', 0.0)
        )
        
        db.session.add(course)
        db.session.commit()
        
        return jsonify({
            'message': 'Course created successfully',
            'course': course.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/courses/<course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    """Update course details"""
    try:
        user_id = get_jwt_identity()
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            course.name = data['name']
        if 'description' in data:
            course.description = data['description']
        if 'category' in data:
            course.category = data['category']
        if 'level' in data:
            course.level = data['level']
        if 'duration' in data:
            course.duration = data['duration']
        if 'instructor' in data:
            course.instructor = data['instructor']
        if 'is_active' in data:
            course.is_active = data['is_active']
        if 'price' in data:
            course.price = data['price']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Course updated successfully',
            'course': course.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/courses/<course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    """Delete course (soft delete)"""
    try:
        user_id = get_jwt_identity()
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        course.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Course deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/initialize-courses', methods=['POST'])
@jwt_required()
def initialize_courses():
    """Initialize all courses from INITIAL_COURSES"""
    try:
        user_id = get_jwt_identity()
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        # Check if courses already exist
        if Course.query.count() > 0:
            return jsonify({'message': 'Courses already initialized', 'courses_count': Course.query.count()}), 200
        
        # Add all courses
        for course_data in INITIAL_COURSES:
            course = Course(**course_data)
            db.session.add(course)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully initialized {len(INITIAL_COURSES)} courses',
            'courses_count': len(INITIAL_COURSES)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<user_id>/make-admin', methods=['POST'])
@jwt_required()
def make_user_admin(user_id):
    """Promote user to admin"""
    try:
        current_user_id = get_jwt_identity()
        
        if not check_admin(current_user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_admin = True
        db.session.commit()
        
        return jsonify({
            'message': 'User promoted to admin',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user account"""
    try:
        current_user_id = get_jwt_identity()
        
        if not check_admin(current_user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete related data
        Enrollment.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get all platform statistics"""
    try:
        user_id = get_jwt_identity()
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        stats = {
            'users': {
                'total': User.query.filter_by(is_admin=False).count(),
                'admins': User.query.filter_by(is_admin=True).count()
            },
            'courses': {
                'total': Course.query.filter_by(is_active=True).count(),
                'by_category': {
                    'ai': Course.query.filter_by(category='ai', is_active=True).count(),
                    'data': Course.query.filter_by(category='data', is_active=True).count(),
                    'cloud': Course.query.filter_by(category='cloud', is_active=True).count()
                }
            },
            'enrollments': {
                'total': Enrollment.query.count(),
                'active': Enrollment.query.filter_by(status='active').count(),
                'completed': Enrollment.query.filter_by(status='completed').count()
            },
            'messages': {
                'total': ContactMessage.query.count(),
                'replied': ContactMessage.query.filter_by(is_replied=True).count(),
                'pending': ContactMessage.query.filter_by(is_replied=False).count()
            }
        }
        
        return jsonify({'statistics': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/db-status', methods=['GET'])
@jwt_required()
def db_status():
    """Check database status"""
    try:
        user_id = get_jwt_identity()
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        # Try a simple query to verify connection
        User.query.first()
        
        return jsonify({
            'status': 'connected',
            'database': 'SQLite',
            'message': 'Database connection is healthy'
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500
