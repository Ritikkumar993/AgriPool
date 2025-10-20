# 🗄️ Setting Up MongoDB on Railway

## Your Current Error:
```
localhost:27017: Connection refused
```

**Why?** Your Railway app is trying to connect to localhost, but there's no MongoDB running there.

---

## ✅ Solution: Add MongoDB to Railway

### Step 1: Add MongoDB Service

1. Go to your Railway project: https://railway.com/project/fa73ca61-9931-4467-b7e6-28637c03699b
2. Click the **"+ New"** button (top right)
3. Select **"Database"**
4. Choose **"Add MongoDB"**
5. Railway will create a MongoDB instance

### Step 2: Link MongoDB to Your Web Service

Railway should automatically create these variables in your MongoDB service:
- `MONGO_URL`
- `MONGOHOST`
- `MONGOPORT`
- `MONGOUSER`
- `MONGOPASSWORD`

### Step 3: Add Connection String to Web Service

1. Click on your **web service** (the one running Django)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add this variable:

**Variable Name:**
```
MONGODB_URL
```

**Variable Value (use one of these formats):**

**Format 1: Reference MongoDB service**
```
mongodb://${{MongoDB.MONGOUSER}}:${{MongoDB.MONGOPASSWORD}}@${{MongoDB.MONGOHOST}}:${{MongoDB.MONGOPORT}}
```

**Format 2: Use internal Railway networking**
```
mongodb://mongo:password@mongodb.railway.internal:27017
```

**Format 3: Copy from MongoDB service**
- Go to MongoDB service → Variables tab
- Copy the `MONGO_URL` value
- Paste it as `MONGODB_URL` in your web service

### Step 4: Save and Redeploy

1. Click **"Save"** or just close the variable editor
2. Railway will **auto-redeploy** your web service
3. Wait 1-2 minutes
4. Check the logs - you should see "MongoDB connected successfully!"

---

## 🌐 Alternative: Use MongoDB Atlas (Free)

If Railway MongoDB isn't available or you want a free option:

### Step 1: Create MongoDB Atlas Account
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free)
3. Create a **free M0 cluster** (512MB free forever)

### Step 2: Get Connection String
1. Click **"Connect"** on your cluster
2. Choose **"Connect your application"**
3. Copy the connection string:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. Add database name at the end:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/agripool?retryWrites=true&w=majority
   ```

### Step 3: Add to Railway
1. Go to your web service in Railway
2. Variables tab
3. Add:
   ```
   MONGODB_URL = mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/agripool?retryWrites=true&w=majority
   ```

### Step 4: Whitelist Railway IPs
1. In MongoDB Atlas, go to **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Save

---

## 🔍 How to Check if It's Working

### Check Railway Logs:
1. Go to your web service
2. Click **"Deployments"** tab
3. Click the latest deployment
4. Look for:
   ```
   Connecting to MongoDB using connection string...
   MongoDB connected successfully!
   ```

### If You See Errors:
```
MongoDB connection error: ...
```

**Common fixes:**
- Check the `MONGODB_URL` variable is set correctly
- Verify MongoDB service is running
- Check username/password are correct
- For Atlas: verify IP whitelist includes 0.0.0.0/0

---

## 📋 Quick Checklist

- [ ] MongoDB service added to Railway project
- [ ] `MONGODB_URL` variable added to web service
- [ ] Connection string format is correct
- [ ] Web service redeployed
- [ ] Logs show "MongoDB connected successfully!"
- [ ] Website loads without errors

---

## 🎯 Expected Result

After setup:
1. ✅ No more "Connection refused" errors
2. ✅ App starts successfully
3. ✅ Website loads in browser
4. ✅ Can create bookings and see data

---

## 💡 Pro Tip

**For local development**, keep using Docker:
```bash
docker compose up
```

**For Railway**, use the `MONGODB_URL` environment variable.

The code automatically detects which environment you're in!

---

## 🆘 Still Having Issues?

Check these:
1. MongoDB service is running (green status in Railway)
2. `MONGODB_URL` variable exists in web service
3. Connection string doesn't have typos
4. Railway logs show connection attempt
5. No firewall blocking connections (for Atlas)

---

## ✅ Once Working

Your Railway URL will show the full working website:
```
https://your-app.railway.app
```

With MongoDB connected, you can:
- Create transport listings
- Make bookings
- Negotiate prices
- View on map
- Everything works! 🎉
