from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process-payment/', views.process_payment, name='process-payment'),
    path('success/', views.success, name='success'),
] 