import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail
from dotenv import load_dotenv
from functools import wraps

from config import config
from models import db, User, Course, Enrollment, ContactMessage, Testimonial, Statistic

# Load environment variables
load_dotenv()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    Mail(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Please log in'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'message': 'Something went wrong'}), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register API blueprints
    from routes import auth_bp, courses_bp, enrollments_bp, users_bp, contact_bp, admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(enrollments_bp, url_prefix='/api/enrollments')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'institute': app.config['INSTITUTE_NAME']
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'SEC2SYSTEMS Training Platform API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'courses': '/api/courses',
                'enrollments': '/api/enrollments',
                'users': '/api/users',
                'contact': '/api/contact',
                'admin': '/api/admin'
            }
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000, debug=True)
