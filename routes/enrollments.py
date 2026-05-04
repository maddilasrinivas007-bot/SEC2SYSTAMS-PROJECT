from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Enrollment, Course, User

enrollments_bp = Blueprint('enrollments', __name__)

@enrollments_bp.route('', methods=['POST'])
@jwt_required()
def enroll_course():
    """Enroll user in a course"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('course_id') and not data.get('course_name'):
            return jsonify({'error': 'Course ID or name required'}), 400
        
        # Find course
        if data.get('course_id'):
            course = Course.query.get(data['course_id'])
        else:
            course = Course.query.filter_by(name=data['course_name']).first()
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        # Check if already enrolled
        existing = Enrollment.query.filter_by(user_id=user_id, course_id=course.id).first()
        if existing:
            return jsonify({'error': 'Already enrolled in this course'}), 409
        
        # Create enrollment
        enrollment = Enrollment(user_id=user_id, course_id=course.id)
        db.session.add(enrollment)
        db.session.commit()
        
        return jsonify({
            'message': 'Successfully enrolled in course',
            'enrollment': enrollment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/my-enrollments', methods=['GET'])
@jwt_required()
def get_my_enrollments():
    """Get current user's enrollments"""
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status')
        
        query = Enrollment.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        enrollments = query.all()
        
        return jsonify({
            'enrollments': [enrollment.to_dict() for enrollment in enrollments],
            'total': len(enrollments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/<enrollment_id>', methods=['GET'])
def get_enrollment(enrollment_id):
    """Get enrollment details"""
    try:
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        
        return jsonify({'enrollment': enrollment.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/<enrollment_id>', methods=['PUT'])
@jwt_required()
def update_enrollment(enrollment_id):
    """Update enrollment (progress, status)"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        
        # Check authorization
        if enrollment.user_id != user_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        # Update fields
        if 'progress' in data:
            enrollment.progress = min(100, max(0, float(data['progress'])))
        
        if 'status' in data:
            enrollment.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Enrollment updated',
            'enrollment': enrollment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/<enrollment_id>', methods=['DELETE'])
@jwt_required()
def unenroll_course(enrollment_id):
    """Unenroll from a course"""
    try:
        user_id = get_jwt_identity()
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        
        # Check authorization
        if enrollment.user_id != user_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        db.session.delete(enrollment)
        db.session.commit()
        
        return jsonify({'message': 'Unenrolled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/course/<course_id>/students', methods=['GET'])
def get_course_enrollments(course_id):
    """Get all enrollments for a course"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        
        return jsonify({
            'course': course.to_dict(),
            'enrollments': [enrollment.to_dict() for enrollment in enrollments],
            'total_students': len(enrollments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/stats', methods=['GET'])
def get_enrollment_stats():
    """Get enrollment statistics"""
    try:
        total_enrollments = Enrollment.query.count()
        active_enrollments = Enrollment.query.filter_by(status='active').count()
        completed_enrollments = Enrollment.query.filter_by(status='completed').count()
        
        # Average progress
        from sqlalchemy import func
        avg_progress = db.session.query(func.avg(Enrollment.progress)).scalar() or 0
        
        return jsonify({
            'total_enrollments': total_enrollments,
            'active_enrollments': active_enrollments,
            'completed_enrollments': completed_enrollments,
            'average_progress': round(avg_progress, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
