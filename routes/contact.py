from flask import Blueprint, request, jsonify
from models import db, ContactMessage
from email_validator import validate_email, EmailNotValidError

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/submit', methods=['POST'])
def submit_contact_form():
    """Submit contact form"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email
        try:
            valid = validate_email(data['email'])
            email = valid.email
        except EmailNotValidError as e:
            return jsonify({'error': f'Invalid email: {str(e)}'}), 400
        
        # Create contact message
        message = ContactMessage(
            name=data['name'],
            email=email,
            subject=data['subject'],
            message=data['message'],
            phone=data.get('phone')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact form submitted successfully. We will get back to you soon.',
            'contact_id': message.id,
            'submitted_at': message.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@contact_bp.route('/messages', methods=['GET'])
def get_contact_messages():
    """Get all contact messages (admin only)"""
    try:
        # In production, add admin authentication check here
        status = request.args.get('status')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = ContactMessage.query
        
        if status == 'replied':
            query = query.filter_by(is_replied=True)
        elif status == 'pending':
            query = query.filter_by(is_replied=False)
        
        total = query.count()
        messages = query.order_by(ContactMessage.created_at.desc()).limit(limit).offset(offset).all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages],
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contact_bp.route('/messages/<message_id>', methods=['GET'])
def get_contact_message(message_id):
    """Get specific contact message"""
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        return jsonify({'message': message.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contact_bp.route('/messages/<message_id>/reply', methods=['POST'])
def reply_to_message(message_id):
    """Reply to contact message (admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('reply_message'):
            return jsonify({'error': 'Reply message required'}), 400
        
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        message.is_replied = True
        message.reply_message = data['reply_message']
        db.session.commit()
        
        return jsonify({
            'message': 'Reply sent successfully',
            'contact': message.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@contact_bp.route('/messages/<message_id>', methods=['DELETE'])
def delete_contact_message(message_id):
    """Delete contact message (admin only)"""
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({'message': 'Message deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@contact_bp.route('/stats', methods=['GET'])
def get_contact_stats():
    """Get contact form statistics"""
    try:
        total_messages = ContactMessage.query.count()
        replied_messages = ContactMessage.query.filter_by(is_replied=True).count()
        pending_messages = total_messages - replied_messages
        
        return jsonify({
            'total_messages': total_messages,
            'replied': replied_messages,
            'pending': pending_messages,
            'reply_rate': round((replied_messages / total_messages * 100) if total_messages > 0 else 0, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
