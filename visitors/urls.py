from django.urls import path
from .views import Register
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',Register.as_view(),name = 'register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'login.html'),name= "Login"),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'logout.html'),name= 'Logout')
]
