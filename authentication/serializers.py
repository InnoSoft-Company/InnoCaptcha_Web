from rest_framework import serializers
from .models import Users

class RegisterationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ("id", "username", "email", "phone", "created_at")

class LoginSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ("username", "email", "phone")
