from django.urls import path
from . import views as v

urlpatterns = [
  path("", v.index, name="index"),
  path("terms/", v.terms, name="terms"),
  path("privacy/", v.privacy, name="privacy"),
]