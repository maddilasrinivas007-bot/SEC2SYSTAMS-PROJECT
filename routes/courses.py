from flask import Blueprint, request, jsonify
from models import db, Course, Enrollment

courses_bp = Blueprint('courses', __name__)

# Course data for initialization
INITIAL_COURSES = [
    {
        'name': 'Generative AI',
        'description': 'Master the latest generative AI models, prompt engineering, and build intelligent applications from scratch.',
        'category': 'ai',
        'icon': 'fas fa-brain',
        'duration': '8 weeks',
        'level': 'Beginner+',
        'instructor': 'AI Expert Team'
    },
    {
        'name': 'Snowflake with Cortex',
        'description': 'Cloud data warehousing with advanced analytics, AI capabilities, and real-time data processing.',
        'category': 'data',
        'icon': 'fas fa-snowflake',
        'duration': '6 weeks',
        'level': 'Intermediate',
        'instructor': 'Data Engineering Team'
    },
    {
        'name': 'Python Programming',
        'description': 'Complete Python mastery: from fundamentals to advanced concepts with real-world projects.',
        'category': 'ai',
        'icon': 'fab fa-python',
        'duration': '10 weeks',
        'level': 'Beginner',
        'instructor': 'Python Experts'
    },
    {
        'name': 'PySpark',
        'description': 'Distributed data processing with Apache Spark using Python for big data applications.',
        'category': 'data',
        'icon': 'fas fa-fire',
        'duration': '7 weeks',
        'level': 'Intermediate',
        'instructor': 'Big Data Team'
    },
    {
        'name': 'Databricks',
        'description': 'Unified analytics platform combining data warehousing, data science, and machine learning.',
        'category': 'data',
        'icon': 'fas fa-database',
        'duration': '8 weeks',
        'level': 'Intermediate',
        'instructor': 'Data Platform Team'
    },
    {
        'name': 'Machine Learning',
        'description': 'Comprehensive ML training covering algorithms, model building, and deployment strategies.',
        'category': 'ai',
        'icon': 'fas fa-microchip',
        'duration': '10 weeks',
        'level': 'Intermediate',
        'instructor': 'ML Specialists'
    },
    {
        'name': 'Deep Learning',
        'description': 'Advanced neural networks, CNNs, RNNs, and transformers for cutting-edge AI applications.',
        'category': 'ai',
        'icon': 'fas fa-project-diagram',
        'duration': '10 weeks',
        'level': 'Advanced',
        'instructor': 'Deep Learning Experts'
    },
    {
        'name': 'AWS DevOps',
        'description': 'Master cloud deployment, CI/CD pipelines, and infrastructure automation on AWS.',
        'category': 'cloud',
        'icon': 'fab fa-aws',
        'duration': '8 weeks',
        'level': 'Intermediate',
        'instructor': 'AWS Certified Professionals'
    },
    {
        'name': 'Agentic AI',
        'description': 'Build autonomous AI agents that can perform complex tasks and make intelligent decisions.',
        'category': 'ai',
        'icon': 'fas fa-robot',
        'duration': '8 weeks',
        'level': 'Advanced',
        'instructor': 'AI Research Team'
    },
    {
        'name': 'Chatbots',
        'description': 'Create intelligent conversational AI systems using NLP and machine learning technologies.',
        'category': 'ai',
        'icon': 'fas fa-comments',
        'duration': '6 weeks',
        'level': 'Intermediate',
        'instructor': 'NLP Specialists'
    },
    {
        'name': 'Chat Assistants',
        'description': 'Build sophisticated chat assistants with context awareness and multi-turn conversations.',
        'category': 'ai',
        'icon': 'fas fa-headset',
        'duration': '6 weeks',
        'level': 'Beginner+',
        'instructor': 'AI Assistants Team'
    },
    {
        'name': 'Prompt Engineering',
        'description': 'Master the art and science of crafting effective prompts for AI models and LLMs.',
        'category': 'ai',
        'icon': 'fas fa-pen-fancy',
        'duration': '4 weeks',
        'level': 'Beginner',
        'instructor': 'AI Prompt Experts'
    },
    {
        'name': 'Data Warehouse',
        'description': 'Design and implement enterprise data warehouses with modern tools and best practices.',
        'category': 'data',
        'icon': 'fas fa-warehouse',
        'duration': '8 weeks',
        'level': 'Intermediate',
        'instructor': 'Data Warehouse Architects'
    }
]

@courses_bp.route('', methods=['GET'])
def get_courses():
    """Get all courses with optional filtering"""
    try:
        category = request.args.get('category')
        level = request.args.get('level')
        
        query = Course.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        if level:
            query = query.filter_by(level=level)
        
        courses = query.all()
        
        return jsonify({
            'courses': [course.to_dict() for course in courses],
            'total': len(courses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    """Get specific course details"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        return jsonify({'course': course.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/by-name/<course_name>', methods=['GET'])
def get_course_by_name(course_name):
    """Get course by name"""
    try:
        course = Course.query.filter_by(name=course_name).first()
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        return jsonify({'course': course.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/category/<category>', methods=['GET'])
def get_courses_by_category(category):
    """Get courses by category"""
    try:
        courses = Course.query.filter_by(category=category, is_active=True).all()
        
        return jsonify({
            'courses': [course.to_dict() for course in courses],
            'category': category,
            'total': len(courses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/search', methods=['GET'])
def search_courses():
    """Search courses by name or description"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        courses = Course.query.filter(
            (Course.name.ilike(f'%{query}%') | 
             Course.description.ilike(f'%{query}%')) &
            (Course.is_active == True)
        ).all()
        
        return jsonify({
            'courses': [course.to_dict() for course in courses],
            'query': query,
            'total': len(courses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/stats', methods=['GET'])
def get_course_stats():
    """Get courses statistics"""
    try:
        total_courses = Course.query.filter_by(is_active=True).count()
        total_enrollments = Enrollment.query.count()
        
        by_category = {}
        for category in ['ai', 'data', 'cloud']:
            count = Course.query.filter_by(category=category, is_active=True).count()
            by_category[category] = count
        
        return jsonify({
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'by_category': by_category,
            'active_courses': total_courses
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
