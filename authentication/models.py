from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class UserManager(BaseUserManager):
  def _normalize_username(self, field): return field.lower()
  def create_user(self, username, email, phone, password=None, **extra_fields):
    if not username: raise ValueError("The Username must be set")
    if not email: raise ValueError("The E-mail must be set")
    if not phone: raise ValueError("The Phone must be set")
    user = self.model(username=self._normalize_username(username), email=self._normalize_username(email), phone=phone, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, username, email, phone, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)
    if extra_fields.get('is_staff') is not True: raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True: raise ValueError('Superuser must have is_superuser=True.')
    return self.create_user(username, email, phone, password, **extra_fields)

class Users(AbstractUser):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  phone = PhoneNumberField(unique=True, region="EG")
  created_at = models.DateTimeField(auto_now_add=True)

  objects = UserManager()
  def save(self, *args, **kwargs):
    self.username, self.email = self.username.lower(), self.email.lower()
    super().save(*args, **kwargs)
  def __str__(self): return self.username

class GoogleOAuth(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField("Users", on_delete=models.CASCADE)
  provider_sub = models.CharField(max_length=255, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self): return "Google OAuth for user: " + self.user.username
