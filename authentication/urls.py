from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views as v

urlpatterns = [
  ## Simple Auth System ##
  path("register/", v.RegisterAPIView.as_view(), name="auth-register"), 
  path("login/", v.LoginAPIView.as_view(), name="auth-login"), 
  path('token/refresh/', TokenRefreshView.as_view(), name='auth-token_refresh'), 
  path("logout/", v.LogoutAPIView.as_view(), name="auth-logout"), 

  ## Reset Password ##
  path("reset-password/", v.ResetPasswordRequestView.as_view(), name="auth-reset_password"),
  path("reset-password/confirm/", v.ResetPasswordConfirmView.as_view(), name="auth-reset_password-confirm"),

]
