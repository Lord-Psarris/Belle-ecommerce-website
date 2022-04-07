from django.urls import path
from . import views

app_name="auth"

urlpatterns = [
    path('create-account/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.sign_out, name="logout")
]