# 🚀 Deployment Guide - Flask Course Management System

## Option 1: PythonAnywhere (Recommended for Beginners)

### Steps:
1. **Sign Up**: Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Create Account**: Choose free tier to start
3. **Create Web App**:
   - Dashboard → Web → Add a new web app
   - Choose Flask framework
   - Python 3.9+ version
4. **Upload Code**:
   - Use Git or upload ZIP file
   - Path: `/home/yourusername/mysite/`
5. **Configure WSGI**:
   ```python
   import sys
   sys.path.append('/home/yourusername/mysite')
   from app import app as application
   ```
6. **Install Dependencies**:
   ```bash
   pip install Flask Flask-Login Flask-MySQLdb Werkzeug PyMySQL
   ```
7. **Set Up Database**:
   - Use PythonAnywhere MySQL
   - Update database credentials in `app.py`

---

## Option 2: Heroku (Free Tier Available)

### Steps:
1. **Install Heroku CLI**:
   ```bash
   npm install -g heroku
   ```
2. **Create Procfile**:
   ```
   web: gunicorn app:app
   ```
3. **Create runtime.txt**:
   ```
   python-3.9.16
   ```
4. **Deploy**:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

---

## Option 3. Vercel (Modern & Free)

### Steps:
1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```
2. **Create vercel.json**:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```
3. **Deploy**:
   ```bash
   vercel --prod
   ```

---

## Option 4: DigitalOcean (Full Control)

### Steps:
1. **Create Droplet**: Ubuntu 20.04+ (starting at $4/month)
2. **Setup Server**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```
3. **Clone & Setup**:
   ```bash
   git clone your-repo
   cd cms
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Configure Nginx**:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       location / {
           proxy_pass http://localhost:5000;
       }
   }
   ```

---

## Option 5: AWS/Azure/GCP (Enterprise)

### Steps:
1. **Create VM Instance**
2. **Setup similar to DigitalOcean**
3. **Configure Domain & SSL**
4. **Use Load Balancer for scaling**

---

## 🔧 Production Configuration

### Update app.py for Production:
```python
import os

# Production settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secure-secret-key')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'your-password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'g1b2')

# Disable debug mode in production
app.config['DEBUG'] = False
```

### Environment Variables:
```bash
export SECRET_KEY='your-very-secure-secret-key'
export MYSQL_HOST='your-database-host'
export MYSQL_USER='your-db-user'
export MYSQL_PASSWORD='your-db-password'
export MYSQL_DB='your-database-name'
```

---

## 📋 Pre-Deployment Checklist

### Security:
- [ ] Change default secret key
- [ ] Use environment variables for credentials
- [ ] Enable HTTPS/SSL
- [ ] Set up database with proper permissions
- [ ] Remove debug mode

### Performance:
- [ ] Use production WSGI server (Gunicorn/Waitress)
- [ ] Set up static file serving
- [ ] Configure database connection pooling
- [ ] Add caching if needed

### Monitoring:
- [ ] Set up error logging
- [ ] Monitor server resources
- [ ] Set up backups
- [ ] Configure alerts

---

## 🚀 Quick Start (PythonAnywhere)

1. **Create Account**: [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Upload Files**: Drag & drop your `cms` folder
3. **Install Dependencies**: 
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure WSGI**: Update the WSGI configuration file
5. **Reload Web App**: Click "Reload" button
6. **Visit Your Site**: `https://yourusername.pythonanywhere.com`

---

## 💡 Tips for Success

1. **Start Small**: Use free tiers first
2. **Test Locally**: Ensure everything works before deploying
3. **Use Git**: Version control makes updates easier
4. **Monitor**: Keep an eye on server logs
5. **Backup**: Regular database backups are essential
6. **Security**: Never commit credentials to Git

---

## 🆘 Common Issues & Solutions

### Database Connection Issues:
- Check firewall settings
- Verify database credentials
- Ensure database server is running

### Static Files Not Loading:
- Configure static file serving
- Check file paths in templates
- Ensure CSS/JS files are accessible

### Import Errors:
- Install all dependencies
- Check Python version compatibility
- Verify virtual environment

---

## 📞 Support

For deployment help:
- Check platform documentation
- Review error logs
- Test with minimal setup first
- Use community forums for specific platforms
