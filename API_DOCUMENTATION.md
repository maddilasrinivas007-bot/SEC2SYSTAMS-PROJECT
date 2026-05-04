# 📚 SEC2SYSTEMS API Documentation

## 🌐 Base URL
```
http://localhost:5000/api
```

---

## 🔑 Authentication

All endpoints marked with `🔐` require JWT token.

### Get Token
```
POST /auth/login
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-123",
    "name": "John Doe",
    "email": "user@example.com"
  }
}
```

### Using Token
Include in request header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📌 General Response Format

### Success Response
```json
{
  "message": "Operation successful",
  "data": {}
}
```

### Error Response
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### HTTP Status Codes
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Server Error

---

## 🔐 Auth Endpoints

### Register User
```
POST /auth/register
```

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "9876543210",
  "experience_level": "beginner"
}
```

**Response:** (201)
```json
{
  "message": "Registration successful",
  "access_token": "...",
  "user": { ... }
}
```

### Login
```
POST /auth/login
```

**Request:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:** (200)
```json
{
  "message": "Login successful",
  "access_token": "...",
  "user": { ... }
}
```

### Get Current User 🔐
```
GET /auth/me
```

**Response:** (200)
```json
{
  "user": {
    "id": "user-123",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "experience_level": "beginner",
    "is_admin": false,
    "created_at": "2024-05-04T10:00:00",
    "enrollments_count": 2
  }
}
```

### Change Password 🔐
```
POST /auth/change-password
```

**Request:**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

**Response:** (200)
```json
{
  "message": "Password changed successfully"
}
```

---

## 📚 Course Endpoints

### Get All Courses
```
GET /courses
```

**Query Parameters:**
- `category` (optional) - ai, data, cloud
- `level` (optional) - Beginner, Intermediate, Advanced

**Response:** (200)
```json
{
  "courses": [
    {
      "id": "course-1",
      "name": "Generative AI",
      "description": "Master the latest AI models...",
      "category": "ai",
      "icon": "fas fa-brain",
      "duration": "8 weeks",
      "level": "Beginner+",
      "instructor": "AI Expert Team",
      "max_students": 30,
      "price": 0.0,
      "is_active": true,
      "enrolled_count": 5,
      "created_at": "2024-05-04T10:00:00"
    }
  ],
  "total": 13
}
```

### Get Course by ID
```
GET /courses/<course_id>
```

**Response:** (200)
```json
{
  "course": { ... }
}
```

### Get Course by Name
```
GET /courses/by-name/<course_name>
```

Example: `GET /courses/by-name/Generative%20AI`

**Response:** (200)
```json
{
  "course": { ... }
}
```

### Get Courses by Category
```
GET /courses/category/<category>
```

Categories: `ai`, `data`, `cloud`

**Response:** (200)
```json
{
  "courses": [...],
  "category": "ai",
  "total": 7
}
```

### Search Courses
```
GET /courses/search?q=<query>
```

**Response:** (200)
```json
{
  "courses": [...],
  "query": "python",
  "total": 1
}
```

### Get Course Statistics
```
GET /courses/stats
```

**Response:** (200)
```json
{
  "total_courses": 13,
  "total_enrollments": 45,
  "by_category": {
    "ai": 7,
    "data": 4,
    "cloud": 2
  },
  "active_courses": 13
}
```

---

## 👥 Enrollment Endpoints

### Enroll in Course 🔐
```
POST /enrollments
```

**Request:**
```json
{
  "course_id": "course-123"
}
```

Or by name:
```json
{
  "course_name": "Generative AI"
}
```

**Response:** (201)
```json
{
  "message": "Successfully enrolled in course",
  "enrollment": {
    "id": "enrollment-1",
    "user": { ... },
    "course": { ... },
    "status": "active",
    "progress": 0.0,
    "certificate_issued": false,
    "enrollment_date": "2024-05-04T10:00:00"
  }
}
```

### Get My Enrollments 🔐
```
GET /enrollments/my-enrollments
```

**Query Parameters:**
- `status` (optional) - active, completed, paused

**Response:** (200)
```json
{
  "enrollments": [...],
  "total": 2
}
```

### Get Enrollment Details
```
GET /enrollments/<enrollment_id>
```

**Response:** (200)
```json
{
  "enrollment": { ... }
}
```

### Update Enrollment 🔐
```
PUT /enrollments/<enrollment_id>
```

**Request:**
```json
{
  "progress": 50.0,
  "status": "active"
}
```

**Response:** (200)
```json
{
  "message": "Enrollment updated",
  "enrollment": { ... }
}
```

### Unenroll from Course 🔐
```
DELETE /enrollments/<enrollment_id>
```

**Response:** (200)
```json
{
  "message": "Unenrolled successfully"
}
```

### Get Course Enrollments
```
GET /enrollments/course/<course_id>/students
```

**Response:** (200)
```json
{
  "course": { ... },
  "enrollments": [...],
  "total_students": 5
}
```

### Get Enrollment Statistics
```
GET /enrollments/stats
```

**Response:** (200)
```json
{
  "total_enrollments": 45,
  "active_enrollments": 35,
  "completed_enrollments": 10,
  "average_progress": 35.5
}
```

---

## 👤 User Endpoints

### Get User Profile 🔐
```
GET /users/profile
```

**Response:** (200)
```json
{
  "user": {
    "id": "user-123",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "experience_level": "beginner",
    "is_admin": false,
    "created_at": "2024-05-04T10:00:00",
    "enrollments_count": 2
  }
}
```

### Update Profile 🔐
```
PUT /users/profile
```

**Request:**
```json
{
  "name": "John Doe Updated",
  "phone": "9876543211",
  "experience_level": "intermediate"
}
```

**Response:** (200)
```json
{
  "message": "Profile updated successfully",
  "user": { ... }
}
```

### Get User by ID
```
GET /users/<user_id>
```

**Response:** (200)
```json
{
  "user": { ... }
}
```

### Search Users
```
GET /users/search?q=<query>
```

**Response:** (200)
```json
{
  "users": [...],
  "total": 2
}
```

### Get User Statistics
```
GET /users/stats
```

**Response:** (200)
```json
{
  "total_users": 45,
  "admin_users": 1,
  "active_users": 35,
  "by_experience": {
    "beginner": 20,
    "intermediate": 15,
    "advanced": 10
  }
}
```

### Get User Enrollments
```
GET /users/<user_id>/enrollments
```

**Response:** (200)
```json
{
  "user": { ... },
  "enrollments": [...],
  "total": 2
}
```

---

## 📧 Contact Endpoints

### Submit Contact Form
```
POST /contact/submit
```

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Course Inquiry",
  "message": "I want to know more about AI course",
  "phone": "9876543210"
}
```

**Response:** (201)
```json
{
  "message": "Contact form submitted successfully",
  "contact_id": "msg-1",
  "submitted_at": "2024-05-04T10:00:00"
}
```

### Get Contact Messages
```
GET /contact/messages
```

**Query Parameters:**
- `status` (optional) - replied, pending
- `limit` (optional, default: 50)
- `offset` (optional, default: 0)

**Response:** (200)
```json
{
  "messages": [...],
  "total": 15,
  "limit": 50,
  "offset": 0
}
```

### Get Message Details
```
GET /contact/messages/<message_id>
```

**Response:** (200)
```json
{
  "message": {
    "id": "msg-1",
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Course Inquiry",
    "message": "I want to know more...",
    "phone": "9876543210",
    "is_replied": false,
    "reply_message": null,
    "created_at": "2024-05-04T10:00:00"
  }
}
```

### Reply to Message
```
POST /contact/messages/<message_id>/reply
```

**Request:**
```json
{
  "reply_message": "Thank you for your interest. Please call us at +91 8179066637"
}
```

**Response:** (200)
```json
{
  "message": "Reply sent successfully",
  "contact": { ... }
}
```

### Delete Message
```
DELETE /contact/messages/<message_id>
```

**Response:** (200)
```json
{
  "message": "Message deleted successfully"
}
```

### Get Contact Statistics
```
GET /contact/stats
```

**Response:** (200)
```json
{
  "total_messages": 25,
  "replied": 20,
  "pending": 5,
  "reply_rate": 80.0
}
```

---

## 🔧 Admin Endpoints (🔐 Admin only)

### Admin Dashboard 🔐
```
GET /admin/dashboard
```

**Response:** (200)
```json
{
  "dashboard": {
    "total_users": 45,
    "total_courses": 13,
    "total_enrollments": 120,
    "total_messages": 25,
    "pending_messages": 5,
    "active_enrollments": 100,
    "completed_enrollments": 20
  },
  "timestamp": "2024-05-04T10:00:00"
}
```

### Create Course 🔐
```
POST /admin/courses
```

**Request:**
```json
{
  "name": "New Course",
  "description": "Course description",
  "category": "ai",
  "icon": "fas fa-brain",
  "duration": "8 weeks",
  "level": "Beginner",
  "instructor": "Instructor Name",
  "price": 0.0
}
```

**Response:** (201)
```json
{
  "message": "Course created successfully",
  "course": { ... }
}
```

### Update Course 🔐
```
PUT /admin/courses/<course_id>
```

**Request:** (Any field to update)
```json
{
  "name": "Updated Name",
  "is_active": true
}
```

**Response:** (200)
```json
{
  "message": "Course updated successfully",
  "course": { ... }
}
```

### Delete Course 🔐
```
DELETE /admin/courses/<course_id>
```

**Response:** (200)
```json
{
  "message": "Course deactivated successfully"
}
```

### Initialize 13 Courses 🔐
```
POST /admin/initialize-courses
```

**Response:** (201)
```json
{
  "message": "Successfully initialized 13 courses",
  "courses_count": 13
}
```

### Promote User to Admin 🔐
```
POST /admin/users/<user_id>/make-admin
```

**Response:** (200)
```json
{
  "message": "User promoted to admin",
  "user": { ... }
}
```

### Delete User 🔐
```
DELETE /admin/users/<user_id>
```

**Response:** (200)
```json
{
  "message": "User deleted successfully"
}
```

### Get All Statistics 🔐
```
GET /admin/statistics
```

**Response:** (200)
```json
{
  "statistics": {
    "users": { ... },
    "courses": { ... },
    "enrollments": { ... },
    "messages": { ... }
  }
}
```

### Check Database Status 🔐
```
GET /admin/db-status
```

**Response:** (200)
```json
{
  "status": "connected",
  "database": "SQLite",
  "message": "Database connection is healthy"
}
```

---

## 🏥 Health Check Endpoint

### Health Check
```
GET /health
```

**Response:** (200)
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "institute": "SEC2SYSTEMS"
}
```

---

## 📋 Root Endpoint

### API Info
```
GET /
```

**Response:** (200)
```json
{
  "message": "SEC2SYSTEMS Training Platform API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/health",
    "auth": "/api/auth",
    "courses": "/api/courses",
    "enrollments": "/api/enrollments",
    "users": "/api/users",
    "contact": "/api/contact",
    "admin": "/api/admin"
  }
}
```

---

## 🔗 Quick Links

| Resource | Endpoint | Method | Auth |
|----------|----------|--------|------|
| Register | `/auth/register` | POST | ❌ |
| Login | `/auth/login` | POST | ❌ |
| My Profile | `/users/profile` | GET | 🔐 |
| All Courses | `/courses` | GET | ❌ |
| Enroll | `/enrollments` | POST | 🔐 |
| My Enrollments | `/enrollments/my-enrollments` | GET | 🔐 |
| Contact Form | `/contact/submit` | POST | ❌ |
| Admin Dashboard | `/admin/dashboard` | GET | 🔐 |

---

## 🧪 Testing with cURL

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "phone": "9876543210"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Get Courses
```bash
curl http://localhost:5000/api/courses
```

### Get Profile (with token)
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/users/profile
```

---

## ⚠️ Error Messages

### Common Errors

| Error | Code | Solution |
|-------|------|----------|
| Missing required fields | 400 | Check request body |
| Invalid email | 400 | Verify email format |
| Email already registered | 409 | Use different email |
| User not found | 404 | Check user ID |
| Unauthorized | 401 | Provide valid token |
| Access denied | 403 | Admin access required |
| Course already exists | 409 | Use different name |

---

**API Documentation Complete! 🚀**

Last Updated: May 2024
