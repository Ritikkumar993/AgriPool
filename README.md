# 🌾 AgriPool — Transport Pooling Platform

A modern Django web application for farmers and transporters, enabling **transport pooling** and **cost sharing** for agricultural produce to markets.

## ✨ Features

### For Farmers
- 📦 **Shipment Requests** - Post your produce transport needs with pickup and destination details
- 🗺️ **Interactive Map** - Click on map to select pickup location (no coordinates needed!)
- 🚚 **Find Transport** - Browse available transport options going to your market
- 🤝 **Pool with Others** - Combine shipments with other farmers to share costs
- 📊 **Track Shipments** - Monitor your shipments, pooling status, and bookings in real-time
- 💰 **Save Money** - Reduce transport costs by up to 40% through pooling

### For Transporters
- 🚚 **Transport Offers** - Post available transport routes and capacity
- 🗺️ **Route Preview** - See visual route between pickup and destination on map
- 💰 **Earnings Tracking** - Monitor completed trips and total earnings
- 📋 **Request Management** - Browse and respond to farmer shipment requests

### General
- 🎨 **Beautiful UI** - Modern, responsive design with Tailwind CSS
- 🔐 **Secure Authentication** - Separate login for farmers and transporters
- 📱 **Mobile Responsive** - Works seamlessly on all devices
- 🌐 **RESTful API** - Complete API for mobile app integration

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agripool_mongo_django
   ```

2. **Build and start containers**
   ```bash
   docker compose up --build -d
   ```

3. **Populate demo data**
   ```bash
   docker compose exec web python manage.py populate_demo_data
   ```

4. **Access the application**
   - **Web App**: http://localhost:8000
   - **Mongo Express**: http://localhost:8081
   - **API Docs**: http://localhost:8000/api/

### Demo Credentials
- **Farmer Login**
  - Username: `ramesh_farmer`
  - Password: `demo123`

- **Transporter Login**
  - Username: `transport_raj`
  - Password: `demo123`

## 📁 Project Structure

```
AgriPool/
├── agri/                       # Main Django app
│   ├── models.py              # MongoDB models (Farmer, Parcel, Shipment, etc.)
│   ├── views.py               # API views
│   ├── views_web.py           # Web UI views
│   ├── views_auth.py          # Authentication views
│   ├── serializers.py         # DRF serializers
│   ├── templates/             # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── farmer_dashboard.html
│   │   ├── transporter_dashboard.html
│   │   ├── fertilizer_plan.html
│   │   └── transport_list.html
│   └── management/commands/   # Custom management commands
├── agripool/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🌐 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Parcels
- `GET /api/parcels/` - List all parcels
- `POST /api/parcels/create/` - Create new parcel

### Shipments
- `GET /api/shipments/` - List open shipments
- `POST /api/shipments/create/` - Create new shipment
- `GET /api/shipments/pool/?radius_km=10` - Pool nearby shipments

## 🎨 Technology Stack

- **Backend**: Django 5.2.7
- **Database**: MongoDB (via MongoEngine)
- **API**: Django REST Framework
- **Authentication**: JWT + Session-based
- **Frontend**: Tailwind CSS, Alpine.js, AOS animations
- **Maps**: Leaflet.js + OpenStreetMap (FREE, no API key needed)
- **Geocoding**: Nominatim (FREE)
- **Containerization**: Docker & Docker Compose

## 🛠️ Development

### Run migrations
```bash
docker compose exec web python manage.py migrate
```

### Create custom data
```bash
docker compose exec web python manage.py shell
```

### View logs
```bash
docker compose logs -f web
```

### Restart services
```bash
docker compose restart web
```

### Stop all services
```bash
docker compose down
```

## 📊 Database Models

- **Farmer** - Farmer profile with contact details
- **Transporter** - Transporter profile with vehicle info
- **Parcel** - Land parcel with soil type and location
- **Crop** - Crop types and seasons
- **Shipment** - Shipment requests from farmers
- **TransportOffer** - Available transport from transporters
- **FertilizerPlan** - Customized fertilizer recommendations
- **Feedback** - User feedback and contact messages

## 🔒 Security Features

- Password hashing (SHA-256)
- CSRF protection
- Session management
- JWT authentication for API
- Input validation

## 🚀 Future Enhancements

- [ ] Payment gateway integration
- [ ] Real-time chat between farmers and transporters
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Weather integration
- [ ] Market price tracking
- [ ] SMS notifications

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, email support@agripool.com or create an issue in the repository.
