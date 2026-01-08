from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/pending-registrations/', views.pending_registrations_view, name='pending_registrations'),
    path('admin/pending-registrations/<int:user_id>/approve/', views.approve_registration_view, name='approve_registration'),
    path('admin/pending-registrations/<int:user_id>/reject/', views.reject_registration_view, name='reject_registration'),
]
