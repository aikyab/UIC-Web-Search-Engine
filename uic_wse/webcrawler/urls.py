from django.urls import path, include
from . import views
urlpatterns = [
    path('home/', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
]
