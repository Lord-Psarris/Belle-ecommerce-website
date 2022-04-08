from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('subscribe-to-newsletter/', views.subscribe_to_newsletter, name='subscribe_to_newsletter'),
]