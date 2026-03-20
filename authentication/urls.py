from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views as v

urlpatterns = [
  path("register/", v.RegisterAPIView.as_view(), name="auth-register"), 
  path("login/", v.LoginOTPAPIView.as_view(), name="auth-login"), 
  path('token/refresh/', TokenRefreshView.as_view(), name='auth-token_refresh'), 
  path("logout/", v.LogoutAPIView.as_view(), name="auth-logout"), 

]
