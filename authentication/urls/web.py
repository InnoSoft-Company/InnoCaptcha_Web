from django.urls import path
from ..views import web as v

urlpatterns = [
  ## Auth ##
  path("login/", v.auth.login, name="web-auth-login"),
  path("signup/", v.auth.signup, name="web-auth-signup"),
  path("forgotPassword/", v.auth.logout, name="web-auth-forgotPassword"),
  path("logout/", v.auth.logout, name="web-auth-logout"),
  
  ## Account Center ##
  path("account_center/myProfile/", v.account_center.myProfile, name="web-account_center-myProfile"),
  path("account_center/activate/", v.account_center.activateAccount, name="web-account_center-activate"),
  
  
  ## OAuth ##
  path("OAuth/<str:oauth_provider>/redirect/", v.oauth.oauth_redirect, name="web-auth-oauth-redirect"),
  path("OAuth/<str:oauth_provider>/callback/", v.oauth.oauth_callback, name="web-auth-oauth-callback"),
  
  
]
