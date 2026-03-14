from django.urls import path, include
from . import views as v

urlpatterns = [
  path('api/contact/submit/', v.contactSubmit, name="api-contact-submit"),
    
]