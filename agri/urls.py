from django.urls import path
from . import views, views_auth, views_web

urlpatterns = [
    # Web UI Routes
    path('', views_web.home, name='home'),
    path('login/', views_web.login_view, name='login'),
    path('register/', views_web.register_view, name='register'),
    path('logout/', views_web.logout_view, name='logout'),
    path('farmer/dashboard/', views_web.farmer_dashboard, name='farmer_dashboard'),
    path('transporter/dashboard/', views_web.transporter_dashboard, name='transporter_dashboard'),
    path('shipment/create/', views_web.create_shipment, name='create_shipment'),
    path('transport/', views_web.transport_list, name='transport_list'),
    path('transport/add/', views_web.add_transport_offer, name='add_transport_offer'),
    path('transport/book/<str:offer_id>/', views_web.book_transport, name='book_transport'),
    path('booking/confirmation/<str:booking_id>/', views_web.booking_confirmation, name='booking_confirmation'),
    path('bookings/', views_web.my_bookings, name='my_bookings'),
    path('transporter/bookings/', views_web.transporter_bookings, name='transporter_bookings'),
    path('booking/update/<str:booking_id>/', views_web.update_booking_status, name='update_booking_status'),
    path('booking/negotiate/<str:booking_id>/', views_web.respond_to_negotiation, name='respond_to_negotiation'),
    path('booking/counter-response/<str:booking_id>/', views_web.respond_to_counter_offer, name='respond_to_counter_offer'),
    path('contact/', views_web.contact, name='contact'),
    
    # API Routes
    path('api/shipments/', views.ListShipmentsView.as_view(), name='shipments-list'),
    path('api/shipments/create/', views.CreateShipmentView.as_view(), name='shipments-create'),
    path('api/shipments/pool/', views.pool_shipments, name='shipments-pool'),
    path('api/auth/register/', views_auth.RegisterView.as_view(), name='auth-register'),
]
