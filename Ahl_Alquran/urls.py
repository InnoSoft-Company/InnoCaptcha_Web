from django.views.generic.base import RedirectView
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.templatetags.static import static as static_url
from rest_framework import permissions
from django.conf import settings
from django.contrib import admin
from drf_yasg import openapi

schema_view = get_schema_view(openapi.Info(title="Ahl Alquran APIs", default_version='v1', description="API documentation", ), public=True, permission_classes=[permissions.AllowAny],)

urlpatterns = [
  ## Default URLs ##
  path('favicon.ico', RedirectView.as_view(url=static_url('imgs/favicon.ico'), permanent=True)),
  path('dj-admin/', admin.site.urls),
  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

  ## Project URLs ## 
  path("", include("websiteBackend.urls")),
  path("auth/", include("authentication.urls")),
  
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
