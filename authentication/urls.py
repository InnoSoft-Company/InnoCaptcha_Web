from django.urls import path
from .views import auth as v

urlpatterns = [
  ## Simple Auth System ##
  path("register/", v.register, name="auth-register"), 
  path("login/", v.login, name="auth-login"), 
  path("logout/", v.logout, name="auth-logout"), 

]