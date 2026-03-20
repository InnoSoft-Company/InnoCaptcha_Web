from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("id", "username", "email", "first_name", "last_name", "phone", "created_at")
    read_only_fields = ("id", "created_at")

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, min_length=8)
  class Meta: model, fields = User, ("id", "username", "email", "password", "first_name", "last_name", "phone")
  def create(self, validated_data):
    user = User(**validated_data)
    user.set_password(validated_data.pop("password"))
    user.save()
    return user

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)

class ResetPasswordRequestSerializer(serializers.Serializer): email = serializers.EmailField()

class ResetPasswordConfirmSerializer(serializers.Serializer):
  email = serializers.EmailField()
  token = serializers.CharField()
  new_password = serializers.CharField(min_length=6)
