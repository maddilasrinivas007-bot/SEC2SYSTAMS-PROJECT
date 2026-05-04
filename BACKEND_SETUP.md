# 🚀 Python Backend Setup Guide - SEC2SYSTEMS

## 📋 Overview

Complete Python Flask backend for SEC2SYSTEMS Training Platform with:
- ✅ RESTful API with 6 modules
- ✅ SQLAlchemy ORM with SQLite
- ✅ JWT Authentication
- ✅ Form Validation
- ✅ CORS Support
- ✅ Admin Dashboard
- ✅ 13 Pre-loaded Courses

---

## 🔧 Prerequisites

Before starting, ensure you have:
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ macOS Terminal or Command Prompt

### Check Python Installation
```bash
python --version
python -m pip --version
```

---

## 📦 Installation Steps

### Step 1: Navigate to Project Directory
```bash
cd /Users/maddilasrinivasulu/Desktop/SEC2SYSTAMS\ PROJECT/
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

✅ You should see `(venv)` prefix in terminal

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (Web framework)
- Flask-SQLAlchemy (Database ORM)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-origin support)
- Flask-Mail (Email service)
- python-dotenv (Environment variables)
- email-validator (Email validation)

### Step 4: Create Environment File
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings (optional for development)
# nano .env
```

### Step 5: Initialize Database
```bash
# Create database and seed data
python init_db.py
```

✅ This creates:
- SQLite database (sec2systems.db)
- All tables
- 13 courses
- Sample users
- Admin account
- Testimonials
- Statistics

---

## ▶️ Running the Application

### Start Flask Backend
```bash
# Make sure you're in the project directory with venv activated
python app.py
```

✅ Backend starts on **http://localhost:5000**

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Restarting with reloader
```

### Keep Running
- Keep this terminal open
- Backend will auto-reload on file changes
- Press `Ctrl+C` to stop

---

## 🌐 Connecting Frontend to Backend

### Update Frontend (index.html)
Add this to beginning of `script.js`:

```javascript
// Backend API configuration
const API_BASE_URL = 'http://localhost:5000/api';
const token = localStorage.getItem('access_token');

// Helper function to make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        }
    };
    
    if (data) options.body = JSON.stringify(data);
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    return response.json();
}
```

### Update Frontend Forms
```javascript
// Login Form
enrollmentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const response = await apiCall('/auth/login', 'POST', {
        email: document.getElementById('enrollEmail').value,
        password: document.getElementById('enrollPassword').value
    });
    
    if (response.access_token) {
        localStorage.setItem('access_token', response.access_token);
        showNotification('Login successful!', 'success');
    }
});
```

---

## 📚 API Endpoints

### Authentication (`/api/auth`)
```
POST   /auth/register          Register new user
POST   /auth/login            Login user
GET    /auth/me               Get current user (JWT required)
POST   /auth/change-password  Change password (JWT required)
```

### Courses (`/api/courses`)
```
GET    /courses               Get all courses
GET    /courses/<id>          Get course by ID
GET    /courses/by-name/<name>  Get course by name
GET    /courses/category/<cat>  Get courses by category
GET    /courses/search?q=...  Search courses
GET    /courses/stats         Get course statistics
```

### Enrollments (`/api/enrollments`)
```
POST   /enrollments           Enroll in course (JWT required)
GET    /enrollments/my-enrollments  Get user's enrollments (JWT required)
GET    /enrollments/<id>      Get enrollment details
PUT    /enrollments/<id>      Update enrollment (JWT required)
DELETE /enrollments/<id>      Unenroll from course (JWT required)
GET    /enrollments/course/<id>/students  Get course students
GET    /enrollments/stats     Get enrollment statistics
```

### Users (`/api/users`)
```
GET    /users/profile         Get user profile (JWT required)
PUT    /users/profile         Update profile (JWT required)
GET    /users/<id>           Get user info
GET    /users/search?q=...   Search users
GET    /users/stats          Get user statistics
GET    /users/<id>/enrollments  Get user's enrollments
```

### Contact (`/api/contact`)
```
POST   /contact/submit        Submit contact form
GET    /contact/messages      Get all messages (admin)
GET    /contact/messages/<id>  Get message details
POST   /contact/messages/<id>/reply  Reply to message (admin)
DELETE /contact/messages/<id>  Delete message (admin)
GET    /contact/stats         Get contact statistics
```

### Admin (`/api/admin`)
```
GET    /admin/dashboard       Admin dashboard (admin only)
POST   /admin/courses         Create course (admin)
PUT    /admin/courses/<id>    Update course (admin)
DELETE /admin/courses/<id>    Delete course (admin)
POST   /admin/initialize-courses  Initialize 13 courses
POST   /admin/users/<id>/make-admin  Promote user to admin
DELETE /admin/users/<id>      Delete user (admin)
GET    /admin/statistics      Get all statistics (admin)
GET    /admin/db-status       Check database status (admin)
```

---

## 🔐 Authentication

### Login Example
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@sec2systems.com",
    "password": "admin@123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-123",
    "name": "Admin User",
    "email": "admin@sec2systems.com"
  }
}
```

### Using Token in Requests
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 👥 Default Users

### Admin User
```
Email: admin@sec2systems.com
Password: admin@123
```

### Sample Users
```
Email: rajesh@example.com
Password: password123

Email: priya@example.com
Password: password123

Email: amit@example.com
Password: password123
```

⚠️ **Change these in production!**

---

## 📝 Example API Calls

### Register New User
```javascript
fetch('http://localhost:5000/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    password: 'secure_password',
    phone: '9876543210',
    experience_level: 'beginner'
  })
})
```

### Get All Courses
```javascript
fetch('http://localhost:5000/api/courses')
  .then(r => r.json())
  .then(data => console.log(data.courses))
```

### Enroll in Course
```javascript
fetch('http://localhost:5000/api/enrollments', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    course_name: 'Generative AI'
  })
})
```

### Submit Contact Form
```javascript
fetch('http://localhost:5000/api/contact/submit', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    subject: 'Course Inquiry',
    message: 'I want to know more...',
    phone: '9876543210'
  })
})
```

---

## 🗄️ Database Management

### View Database
```bash
# Install SQLite browser (optional)
# https://sqlitebrowser.org/

# Or use command line
sqlite3 sec2systems.db
.tables
SELECT * FROM users;
.quit
```

### Reset Database
```bash
# WARNING: Deletes all data!
python init_db.py reset
```

### Database Structure
```
users                 - Student and admin accounts
courses              - Training courses (13 pre-loaded)
enrollments          - Student course enrollments
contact_messages     - Contact form submissions
testimonials         - Student reviews
statistics           - Platform statistics
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Address already in use"
**Solution:**
```bash
# Use different port
python -c "from app import create_app; app = create_app(); app.run(port=5001)"

# Or kill existing process
lsof -ti:5000 | xargs kill -9
```

### Issue: Database locked error
**Solution:**
```bash
# Remove database and reinitialize
rm sec2systems.db
python init_db.py
```

### Issue: CORS errors in frontend
**Solution:**
Update CORS_ORIGINS in `.env`:
```
CORS_ORIGINS=http://localhost:8000,http://localhost:5000
```

### Issue: JWT token expired
**Solution:**
- User needs to log in again
- Token expires in 30 days (configurable in config.py)

---

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-factor authentication
2. Create App Password (16-character password)
3. Update `.env`:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
```

### Test Email
```python
from flask_mail import Message
from app import create_app, mail

app = create_app()
with app.app_context():
    msg = Message('Test', recipients=['test@example.com'], body='Test email')
    mail.send(msg)
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Change JWT_SECRET_KEY in .env
- [ ] Set DEBUG=False in .env
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set strong admin password
- [ ] Configure email service
- [ ] Set secure CORS_ORIGINS
- [ ] Use HTTPS
- [ ] Set up SSL certificate
- [ ] Use Gunicorn or uWSGI
- [ ] Monitor logs

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📊 Monitoring

### Check API Health
```bash
curl http://localhost:5000/api/health
```

### Admin Dashboard
```
GET /api/admin/dashboard
Authorization: Bearer <admin_token>
```

### Database Statistics
```
GET /api/admin/statistics
Authorization: Bearer <admin_token>
```

---

## 🔐 Security Best Practices

✅ **Implemented:**
- JWT token authentication
- Password hashing (Werkzeug)
- Email validation
- CORS protection
- SQL injection prevention (SQLAlchemy)

⚠️ **Do Not Forget:**
- Change default passwords
- Use HTTPS in production
- Implement rate limiting
- Add request validation
- Set secure cookies
- Add admin authentication checks
- Implement role-based access control
- Add audit logging

---

## 📚 File Structure

```
/project/
├── app.py                 # Flask application factory
├── config.py              # Configuration settings
├── models.py              # Database models
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Authentication endpoints
│   ├── courses.py         # Course endpoints
│   ├── enrollments.py     # Enrollment endpoints
│   ├── users.py           # User endpoints
│   ├── contact.py         # Contact form endpoints
│   └── admin.py           # Admin endpoints
├── sec2systems.db         # SQLite database (created)
├── venv/                  # Virtual environment (created)
└── venv/lib/python3.x/    # Dependencies (created)
```

---

## 🎓 Learning Resources

### Flask Documentation
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Flask-JWT: https://flask-jwt-extended.readthedocs.io/

### Useful Commands
```bash
# List installed packages
pip list

# Show package details
pip show flask

# Upgrade pip
pip install --upgrade pip

# Create requirements from environment
pip freeze > requirements.txt
```

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database initialized (`python init_db.py`)
- [ ] Backend running (`python app.py`)
- [ ] Frontend can connect to API
- [ ] Courses loaded in database
- [ ] Admin account created
- [ ] Sample users created

---

## 🎉 Next Steps

1. ✅ **Start Backend**: `python app.py`
2. ✅ **Test API**: Visit http://localhost:5000/api/health
3. ✅ **Connect Frontend**: Update frontend to use API
4. ✅ **Test Flows**: Register, login, enroll, contact
5. ✅ **Deploy**: Follow deployment checklist

---

**Ready to build your platform! 🚀**

For issues or questions:
- 📧 Email: info@sec2systems.com
- 📱 Phone: +91 8179066637

*Last Updated: May 2024*
