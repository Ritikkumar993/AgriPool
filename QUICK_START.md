# 🚀 AgriPool - Quick Start Guide

## Prerequisites

Before you begin, ensure you have:
- ✅ Docker Desktop installed and running
- ✅ Git installed
- ✅ A web browser (Chrome, Firefox, Edge, or Safari)

## Step-by-Step Setup

### 1. Start the Application

Open your terminal in the project directory and run:

```bash
docker compose up --build -d
```

**What this does:**
- Builds the Django application container
- Starts MongoDB database
- Starts Mongo Express (database admin UI)
- Runs everything in the background

**Expected output:**
```
✔ Container agripool_mongo                         Started
✔ Container agripool_mongo_django-mongo-express-1  Started
✔ Container agripool_web                           Started
```

### 2. Populate Demo Data

```bash
docker compose exec web python manage.py populate_demo_data
```

**What this does:**
- Creates 6 crop types
- Creates 3 demo farmers
- Creates 2 demo transporters
- Creates sample parcels
- Creates sample transport offers

**Expected output:**
```
Created crop: Wheat
Created crop: Rice
...
Demo data populated successfully!
Demo credentials: username=ramesh_farmer, password=demo123
```

### 3. Access the Application

Open your browser and visit:

**🌾 Main Application**
```
http://localhost:8000
```

**🗄️ Database Admin (Mongo Express)**
```
http://localhost:8081
```

## 🎮 Try It Out!

### As a Farmer

1. **Login**
   - Go to http://localhost:8000/login/
   - Select "Farmer" tab
   - Username: `ramesh_farmer`
   - Password: `demo123`
   - Click "Sign In"

2. **Explore Dashboard**
   - View your statistics
   - See your land parcels
   - Check recent shipments

3. **Add a New Parcel**
   - Click "Add New Parcel"
   - Fill in the details:
     - Name: "East Field"
     - Area: 2.5 hectares
     - Soil Type: Loam
     - Latitude: 18.5204
     - Longitude: 73.8567
   - Click "Add Parcel"

4. **Get Fertilizer Plan**
   - Click "Get Fertilizer Plan"
   - Select a parcel
   - Select a crop (e.g., Wheat)
   - Click "Generate Fertilizer Plan"
   - View your customized recommendations!

5. **Create a Shipment**
   - Click "Create Shipment"
   - Select parcel and crop
   - Enter quantity (e.g., 1000 kg)
   - Set ready dates
   - Enter market destination
   - Click "Create Shipment"

### As a Transporter

1. **Login**
   - Go to http://localhost:8000/login/
   - Select "Transporter" tab
   - Username: `transport_raj`
   - Password: `demo123`
   - Click "Sign In"

2. **Explore Dashboard**
   - View your statistics
   - See your active offers
   - Check completed trips

3. **Post Transport Offer**
   - Click "Post Transport Offer"
   - Fill in details:
     - From: Pune
     - To: Mumbai
     - Capacity: 5000 kg
     - Price: ₹5.50 per kg
     - Available date: Select a future date
   - Click "Post Offer"

4. **Browse Shipment Requests**
   - Click "View All Requests"
   - See available shipments
   - Contact farmers directly

### Browse Transport (No Login Required)

1. Go to http://localhost:8000/transport/
2. Use filters to search:
   - From Location: Pune
   - To Location: Mumbai
   - Min Capacity: 1000 kg
3. Click "Search"
4. View available transport options

## 🛠️ Useful Commands

### View Application Logs
```bash
docker compose logs -f web
```

### Restart the Application
```bash
docker compose restart web
```

### Stop Everything
```bash
docker compose down
```

### Start Again
```bash
docker compose up -d
```

### Access Django Shell
```bash
docker compose exec web python manage.py shell
```

### View Database in Mongo Express
1. Open http://localhost:8081
2. Click on "agripool" database
3. Browse collections (farmer, parcel, shipment, etc.)

## 📱 Test on Mobile

1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4)
   - Mac/Linux: `ifconfig` or `ip addr`

2. On your mobile device (connected to same WiFi):
   - Open browser
   - Go to `http://YOUR_IP:8000`
   - Example: `http://192.168.1.100:8000`

## 🎨 Features to Explore

### Home Page
- ✨ Animated hero section
- 📊 Statistics counters
- 💬 Testimonials carousel
- 🎯 Call-to-action buttons

### Dashboards
- 📈 Real-time statistics
- 🗂️ Data tables
- 🎨 Beautiful cards
- ⚡ Quick actions

### Forms
- ✅ Input validation
- 🎭 Interactive elements
- 📱 Mobile-friendly
- 🌈 Visual feedback

## 🐛 Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```bash
# Stop the conflicting service or change port in docker-compose.yml
ports:
  - '8001:8000'  # Change 8000 to 8001
```

### Container Won't Start
```bash
# Check logs
docker compose logs web

# Rebuild from scratch
docker compose down
docker compose up --build -d
```

### Database Connection Error
```bash
# Restart MongoDB
docker compose restart mongo

# Wait a few seconds, then restart web
docker compose restart web
```

### Can't Access from Browser
1. Check if containers are running:
   ```bash
   docker compose ps
   ```

2. All should show "Up" status

3. Try accessing:
   - http://localhost:8000
   - http://127.0.0.1:8000

## 📚 Next Steps

1. **Explore the API**
   - Visit http://localhost:8000/api/parcels/
   - Try other API endpoints
   - Use Postman or curl for testing

2. **Customize the Application**
   - Modify templates in `agri/templates/`
   - Update models in `agri/models.py`
   - Add new features in `agri/views_web.py`

3. **Add Your Own Data**
   - Register new users
   - Create real parcels
   - Post actual transport offers

4. **Read the Documentation**
   - See README.md for full documentation
   - Check PROJECT_SUMMARY.md for technical details

## 🎉 You're All Set!

Enjoy exploring AgriPool! If you encounter any issues, check the troubleshooting section or create an issue on GitHub.

**Happy Farming! 🌾**
