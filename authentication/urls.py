from django.urls import path
from . import views as v

urlpatterns = [
    path('login/', v.LoginView.as_view(), name='auth-login'),
]
