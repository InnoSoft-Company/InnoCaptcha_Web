from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
  list_display = ('username', 'email', 'phone', 'role', 'first_name', 'last_name', 'is_active', 'is_staff')
  list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
  search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
  list_editable = ('role', 'is_active')
  ordering = ('-created_at',)

  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('المعلومات الشخصية', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
    ('الدور والصلاحيات', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ('التواريخ', {'fields': ('last_login', 'date_joined', 'created_at')}),
  )
  readonly_fields = ('created_at', 'last_login', 'date_joined')

  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('username', 'email', 'phone', 'first_name', 'last_name', 'role', 'password1', 'password2'),
    }),
  )

  def save_model(self, request, obj, form, change):
    obj.username, obj.email = obj.username.lower(), obj.email.lower()
    super().save_model(request, obj, form, change)

admin.site.register(GoogleOAuth)
admin.site.register(PasswordResetToken)
