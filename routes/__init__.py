from .auth import auth_bp
from .courses import courses_bp
from .enrollments import enrollments_bp
from .users import users_bp
from .contact import contact_bp
from .admin import admin_bp

__all__ = [
    'auth_bp',
    'courses_bp',
    'enrollments_bp',
    'users_bp',
    'contact_bp',
    'admin_bp'
]
