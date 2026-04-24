from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path ('create_field/', views.create_field, name="create_field"),
    path ('update_field/<int:field_id>/', views.update_field, name="update_field"),]