from django.urls import path
from ..views import api as v

urlpatterns = [
  path("check_username/", v.auth.check_username, name="api-auth-check_username"),
  path("check_email/", v.auth.check_email, name="api-auth-check_email"),
  #path("signup/", v.auth.signup, name="web-signup"),
  
]
