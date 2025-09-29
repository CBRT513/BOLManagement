from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Main menu
    path('', views.MainMenuView.as_view(), name='main_menu'),
    
    # Items
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<uuid:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/<uuid:pk>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/<uuid:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # Sizes
    path('sizes/', views.SizeListView.as_view(), name='size_list'),
    path('sizes/create/', views.SizeCreateView.as_view(), name='size_create'),
    path('sizes/<uuid:pk>/delete/', views.SizeDeleteView.as_view(), name='size_delete'),
    
    # Suppliers
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<uuid:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<uuid:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<uuid:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Customers
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<uuid:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<uuid:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<uuid:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Carriers
    path('carriers/', views.CarrierListView.as_view(), name='carrier_list'),
    path('carriers/create/', views.CarrierCreateView.as_view(), name='carrier_create'),
    path('carriers/<uuid:pk>/', views.CarrierDetailView.as_view(), name='carrier_detail'),
    path('carriers/<uuid:pk>/update/', views.CarrierUpdateView.as_view(), name='carrier_update'),
    path('carriers/<uuid:pk>/delete/', views.CarrierDeleteView.as_view(), name='carrier_delete'),
    
    # Trucks
    path('trucks/', views.TruckListView.as_view(), name='truck_list'),
    path('trucks/create/', views.TruckCreateView.as_view(), name='truck_create'),
    path('trucks/<uuid:pk>/', views.TruckDetailView.as_view(), name='truck_detail'),
    path('trucks/<uuid:pk>/update/', views.TruckUpdateView.as_view(), name='truck_update'),
    path('trucks/<uuid:pk>/delete/', views.TruckDeleteView.as_view(), name='truck_delete'),
    
    # Locations
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/create/', views.LocationCreateView.as_view(), name='location_create'),
    path('locations/<uuid:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('locations/<uuid:pk>/update/', views.LocationUpdateView.as_view(), name='location_update'),
    path('locations/<uuid:pk>/delete/', views.LocationDeleteView.as_view(), name='location_delete'),
    
    # Batches
    path('batches/', views.BatchListView.as_view(), name='batch_list'),
    path('batches/create/', views.BatchCreateView.as_view(), name='batch_create'),
    path('batches/<uuid:pk>/', views.BatchDetailView.as_view(), name='batch_detail'),
    path('batches/<uuid:pk>/update/', views.BatchUpdateView.as_view(), name='batch_update'),
    path('batches/<uuid:pk>/delete/', views.BatchDeleteView.as_view(), name='batch_delete'),
    
    # API Endpoints (for AJAX calls matching your existing system)
    path('api/items/', views.ItemAPIView.as_view(), name='api_items'),
    path('api/sizes/', views.SizeAPIView.as_view(), name='api_sizes'),
    path('api/suppliers/', views.SupplierAPIView.as_view(), name='api_suppliers'),
    path('api/customers/', views.CustomerAPIView.as_view(), name='api_customers'),
    path('api/carriers/', views.CarrierAPIView.as_view(), name='api_carriers'),
    path('api/trucks/', views.TruckAPIView.as_view(), name='api_trucks'),
    path('api/locations/', views.LocationAPIView.as_view(), name='api_locations'),
    path('api/batches/', views.BatchAPIView.as_view(), name='api_batches'),
    
    # Reports
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    # Health check
    path('health/', views.health_check, name='health_check'),
]