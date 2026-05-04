from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Enrollment

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update allowed fields
        if 'name' in data:
            user.name = data['name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'experience_level' in data:
            user.experience_level = data['experience_level']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user information"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by name or email"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        users = User.query.filter(
            (User.name.ilike(f'%{query}%') | User.email.ilike(f'%{query}%')) &
            (User.is_admin == False)
        ).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/stats', methods=['GET'])
def get_user_stats():
    """Get user statistics"""
    try:
        total_users = User.query.filter_by(is_admin=False).count()
        admin_users = User.query.filter_by(is_admin=True).count()
        
        # Users by experience level
        by_experience = {}
        for level in ['beginner', 'intermediate', 'advanced']:
            count = User.query.filter_by(experience_level=level, is_admin=False).count()
            by_experience[level] = count
        
        # Total active users (with enrollments)
        active_users = db.session.query(User.id).distinct(User.id).join(
            Enrollment
        ).count()
        
        return jsonify({
            'total_users': total_users,
            'admin_users': admin_users,
            'active_users': active_users,
            'by_experience': by_experience
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>/enrollments', methods=['GET'])
def get_user_enrollments(user_id):
    """Get user's enrollments"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'user': user.to_dict(),
            'enrollments': [enrollment.to_dict() for enrollment in enrollments],
            'total': len(enrollments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
