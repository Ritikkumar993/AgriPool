# 🚀 AgriPool Deployment Guide

## Quick Deploy Options

### 1️⃣ Railway.app (Recommended - Easiest)

**Why Railway?**
- ✅ Free $5 credit/month
- ✅ Auto-detects Docker
- ✅ One-click MongoDB
- ✅ Automatic HTTPS
- ✅ GitHub integration

**Steps:**

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/agripool.git
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-deploys! 🎉

3. **Add MongoDB**
   - In Railway dashboard, click "New"
   - Select "Database" → "MongoDB"
   - Copy connection string
   - Add to environment variables

4. **Set Environment Variables**
   ```
   DJANGO_SECRET_KEY=your-random-secret-key
   DJANGO_DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   MONGO_HOST=mongodb-host-from-railway
   MONGO_PORT=27017
   MONGO_DBNAME=agripool
   ```

5. **Access Your App**
   - Railway provides URL: `https://your-app.railway.app`
   - Done! ✅

---

### 2️⃣ Render.com (Good Free Tier)

**Steps:**

1. **Push to GitHub** (same as above)

2. **Deploy on Render**
   - Go to https://render.com
   - Sign up
   - New → Web Service
   - Connect GitHub repo
   - Environment: Docker
   - Click "Create Web Service"

3. **Add MongoDB**
   - Use MongoDB Atlas (free tier)
   - Or Render's MongoDB add-on

4. **Set Environment Variables** (in Render dashboard)

5. **Deploy!**

---

### 3️⃣ DigitalOcean (Professional)

**Cost:** $5-10/month

**Steps:**

1. **Create Droplet**
   ```bash
   # Choose Ubuntu 22.04
   # Size: Basic $6/month
   ```

2. **SSH into Server**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Install Docker Compose
   apt install docker-compose -y
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/agripool.git
   cd agripool
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   nano .env
   # Edit with your settings
   ```

6. **Start Application**
   ```bash
   docker compose up -d
   docker compose exec web python manage.py populate_demo_data
   ```

7. **Configure Domain**
   - Point your domain to server IP
   - Install Nginx
   - Setup SSL with Let's Encrypt

---

### 4️⃣ AWS (Enterprise Scale)

**Services:**
- ECS (Container Service)
- DocumentDB (MongoDB)
- ALB (Load Balancer)
- Route 53 (DNS)

**Cost:** ~$30-50/month

**Steps:**
1. Create ECS cluster
2. Push Docker image to ECR
3. Create task definition
4. Setup DocumentDB
5. Configure ALB
6. Deploy!

---

## 📦 Pre-Deployment Steps

### 1. Update docker-compose.yml for Production

```yaml
version: '3.8'
services:
  web:
    build: .
    container_name: agripool_web
    command: gunicorn agripool.wsgi:application --bind 0.0.0.0:8000 --workers 4
    ports:
      - '8000:8000'
    depends_on:
      - mongo
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DJANGO_DEBUG=${DJANGO_DEBUG:-False}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - MONGO_HOST=${MONGO_HOST}
      - MONGO_PORT=${MONGO_PORT}
      - MONGO_DBNAME=${MONGO_DBNAME}
    restart: always

  mongo:
    image: mongo:6.0
    container_name: agripool_mongo
    ports:
      - '27017:27017'
    volumes:
      - mongo_data:/data/db
    restart: always

volumes:
  mongo_data:
```

### 2. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Update settings.py

Add to `agripool/settings.py`:
```python
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'changeme-for-dev')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
```

---

## 🔒 Security Checklist

Before deploying:

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong MongoDB password
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall
- [ ] Regular backups
- [ ] Update dependencies

---

## 🌐 Domain Setup

### Option 1: Use Platform Domain
- Railway: `your-app.railway.app`
- Render: `your-app.onrender.com`

### Option 2: Custom Domain

1. **Buy domain** (Namecheap, GoDaddy, etc.)

2. **Point to your server**
   - Add A record: `@` → `your-server-ip`
   - Add A record: `www` → `your-server-ip`

3. **Setup SSL**
   ```bash
   # Install Certbot
   apt install certbot python3-certbot-nginx
   
   # Get certificate
   certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

---

## 📊 Monitoring

### Setup Monitoring

1. **Application Logs**
   ```bash
   docker compose logs -f web
   ```

2. **Database Monitoring**
   - Use MongoDB Atlas monitoring
   - Or setup Prometheus + Grafana

3. **Uptime Monitoring**
   - UptimeRobot (free)
   - Pingdom
   - StatusCake

---

## 🔄 CI/CD (Optional)

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Railway
        run: |
          # Railway auto-deploys on push
          echo "Deployed!"
```

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid | Best For |
|----------|-----------|------|----------|
| Railway | $5 credit | $5+/month | Quick deploy |
| Render | Yes | $7+/month | Startups |
| DigitalOcean | No | $6+/month | Full control |
| AWS | Limited | $30+/month | Enterprise |
| Heroku | No | $5+/month | Simple apps |

---

## 🆘 Troubleshooting

### App won't start
```bash
# Check logs
docker compose logs web

# Restart
docker compose restart web
```

### Database connection error
```bash
# Check MongoDB is running
docker compose ps

# Restart MongoDB
docker compose restart mongo
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - '8001:8000'
```

---

## 📞 Support

- **Documentation**: See README.md
- **Issues**: Create GitHub issue
- **Email**: support@agripool.com

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] .env configured
- [ ] SECRET_KEY changed
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS set
- [ ] MongoDB configured
- [ ] Domain pointed (if custom)
- [ ] SSL enabled
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Demo data populated
- [ ] Tested all features

---

**Ready to deploy? Choose your platform and follow the steps above!** 🚀
