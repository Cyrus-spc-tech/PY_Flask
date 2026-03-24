# Course Management System (CMS)

A comprehensive course management system built with Flask and MySQL, featuring modern glassmorphism UI, user authentication, role-based access control, and complete course administration capabilities.

## 📁 Project Structure

```
cms/
├── app.py                 # Main Flask application
├── templates/              # HTML templates
│   ├── index.html         # Home page with navigation
│   ├── login.html        # Login form with glassmorphism
│   ├── signup.html       # Registration form
│   ├── dashboard.html    # User dashboard (role-based)
│   ├── admin_dashboard.html # Admin-specific dashboard
│   ├── courses.html      # Course catalog with search/filter
│   ├── course_details.html # Individual course view
│   └── create_course.html # Course creation form
├── static/               # Static assets
│   ├── login.css        # Glassmorphism styling
│   ├── index.css        # Additional styles
│   └── (video files)   # Background media
├── requirements.txt      # Python dependencies
├── config.py           # Configuration settings
└── README.md          # This documentation
```

## 👥 User Roles

### **Student**

- Browse available courses
- View course details
- Enroll in courses
- Track assignments

### **Instructor**

- Create and manage courses
- View enrolled students
- Manage course content
- Track student progress

### **Admin**

- Full system administration
- User management
- Course oversight
- System statistics
