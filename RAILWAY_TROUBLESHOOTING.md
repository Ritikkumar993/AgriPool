# 🚂 Railway Deployment Troubleshooting

## ✅ Build Succeeded but Site Not Loading?

### Common Issues & Fixes

---

## Issue 1: MongoDB Not Connected ⚠️

**Symptom:** Build succeeds, but app crashes on start

**Solution:**

### A. Add MongoDB Plugin to Railway

1. In Railway dashboard, click **"New"**
2. Select **"Database"** → **"Add MongoDB"**
3. Wait for provisioning (2-3 minutes)
4. MongoDB will be available at: `mongo.railway.internal`

### B. Set Environment Variables

In your **web service** (not MongoDB), go to **"Variables"** tab:

```
MONGODB_URL=mongodb://mongo.railway.internal:27017/agripool
DEBUG=False
DJANGO_SECRET_KEY=your-random-secret-key-change-this
ALLOWED_HOSTS=your-app-name.up.railway.app
```

**Important:** Replace `your-app-name` with your actual Railway app name!

### C. Redeploy

After adding variables:
- Railway auto-redeploys
- Or click **"Deploy"** → **"Redeploy"**

---

## Issue 2: Port Binding Error ⚠️

**Symptom:** Logs show "Address already in use" or port errors

**Solution:** Already fixed in updated Dockerfile!

The Dockerfile now uses: `${PORT:-8000}`
- Railway sets `$PORT` dynamically
- Falls back to 8000 for local

---

## Issue 3: Static Files Not Loading ⚠️

**Symptom:** Site loads but no CSS/styling

**Solution:** We're using CDN (Tailwind, Leaflet) so this shouldn't be an issue!

If needed, add to settings.py:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

---

## Issue 4: ALLOWED_HOSTS Error ⚠️

**Symptom:** "Invalid HTTP_HOST header"

**Solution:** Set in Railway Variables:
```
ALLOWED_HOSTS=your-app.up.railway.app,your-app.railway.app
```

Or use wildcard for testing:
```
ALLOWED_HOSTS=*
```

---

## Issue 5: Application Crash Loop ⚠️

**Symptom:** App keeps restarting

**Check Railway Logs for:**

### A. MongoDB Connection Error
```
pymongo.errors.ServerSelectionTimeoutError
```
**Fix:** Add MongoDB plugin and set MONGODB_URL

### B. Missing Dependencies
```
ModuleNotFoundError: No module named 'X'
```
**Fix:** Add to requirements.txt and redeploy

### C. Port Already in Use
```
OSError: [Errno 98] Address already in use
```
**Fix:** Already fixed in Dockerfile (uses $PORT)

---

## 🔍 How to Check Logs in Railway

1. Go to Railway dashboard
2. Click on your **web service**
3. Click **"Deployments"** tab
4. Click on latest deployment
5. Click **"View Logs"**
6. Look for errors (red text)

---

## ✅ Correct Railway Setup

### Your Railway Project Should Have:

1. **Web Service** (your Django app)
   - Source: GitHub repository
   - Builder: Dockerfile
   - Environment Variables set

2. **MongoDB Database** (separate service)
   - Type: MongoDB plugin
   - Connected to web service

### Environment Variables Needed:

```bash
# In Web Service Variables:
MONGODB_URL=mongodb://mongo.railway.internal:27017/agripool
DEBUG=False
DJANGO_SECRET_KEY=generate-random-key-here
ALLOWED_HOSTS=your-app.up.railway.app
```

---

## 🎯 Step-by-Step Fix

### 1. Check Current Status

In Railway:
- Is MongoDB service running? (green dot)
- Is web service running? (green dot)
- Click web service → Check logs

### 2. Add MongoDB if Missing

- Click "New" → "Database" → "MongoDB"
- Wait for green status

### 3. Connect MongoDB to Web Service

Railway should auto-connect, but verify:
- Web service Variables should show MongoDB connection
- Or manually add `MONGODB_URL`

### 4. Set Required Variables

In web service Variables tab, add:
```
MONGODB_URL=mongodb://mongo.railway.internal:27017/agripool
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}
DEBUG=False
```

### 5. Redeploy

- Click "Deploy" → "Redeploy"
- Watch logs for errors
- Wait 2-3 minutes

### 6. Test Your Site

- Click "Open App" button in Railway
- Or visit: `https://your-app.up.railway.app`

---

## 🆘 Still Not Working?

### Check These:

1. **MongoDB Running?**
   ```
   Railway Dashboard → MongoDB service → Should be green
   ```

2. **Web Service Logs?**
   ```
   Look for:
   - "Starting gunicorn" ✅
   - "Booting worker" ✅
   - "Listening at: http://0.0.0.0:XXXX" ✅
   ```

3. **Environment Variables Set?**
   ```
   Web Service → Variables → Should have MONGODB_URL
   ```

4. **Domain Working?**
   ```
   Web Service → Settings → Should show public domain
   ```

---

## 📋 Quick Checklist

- [ ] MongoDB plugin added to Railway
- [ ] MongoDB is running (green status)
- [ ] MONGODB_URL variable set in web service
- [ ] ALLOWED_HOSTS variable set
- [ ] DEBUG=False set
- [ ] App redeployed after adding variables
- [ ] Logs show "Listening at: http://..."
- [ ] Public domain is accessible

---

## 🎬 Video Tutorial

If still stuck, watch:
- Railway Official Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

## 💡 Alternative: Use MongoDB Atlas (External)

If Railway MongoDB isn't working:

1. **Create MongoDB Atlas Account** (free)
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up (free tier)
   - Create cluster (free M0)

2. **Get Connection String**
   - Click "Connect"
   - Choose "Connect your application"
   - Copy connection string

3. **Add to Railway Variables**
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/agripool
   ```

4. **Redeploy**

---

## ✅ Success Indicators

Your app is working when you see in logs:
```
Starting AgriPool on Railway...
Running migrations...
Starting Gunicorn...
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:XXXX
[INFO] Booting worker with pid: X
```

And when you visit the URL, you see the AgriPool homepage! 🎉

---

**Need more help? Share the Railway logs and I can help debug!**
