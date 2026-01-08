from django.urls import path
from . import views

app_name = 'lumbering_service'

urlpatterns = [
    # Dashboard & List views
    path('', views.lumbering_dashboard, name='dashboard'),
    path('orders/', views.lumbering_order_list, name='order_list'),
    
    # Order CRUD
    path('orders/create/', views.lumbering_order_create, name='order_create'),
    path('orders/<int:pk>/', views.lumbering_order_detail, name='order_detail'),
    path('orders/<int:pk>/mark-completed/', views.lumbering_order_mark_completed, name='order_mark_completed'),
    
    # Output management
    path('orders/<int:order_pk>/outputs/create/', views.lumbering_output_create, name='output_create'),
    
    # Shavings management
    path('orders/<int:order_pk>/shavings/create/', views.lumbering_shavings_create, name='shavings_create'),
    
    # Walk-in customer creation
    path('api/create-walkin-customer/', views.create_walkin_customer, name='api_create_walkin_customer'),
]
