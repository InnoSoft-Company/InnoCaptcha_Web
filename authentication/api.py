from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ResetPasswordRequestSerializer, ResetPasswordConfirmSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PasswordResetToken
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from core import utils

User = get_user_model()

class LoginAPIView(APIView):
  permission_classes = (permissions.AllowAny,)
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(request, username=serializer.validated_data["username"], password=serializer.validated_data["password"])
    if not user: return Response({"status": False, "message": "Username or password is incorrect."}, status=401)
    data = UserSerializer(user).data
    login(request, user)
    return Response({"status": True, "data": data, "tokens": utils.getUserTokens(user)})

class RegisterAPIView(APIView):
  permission_classes = (permissions.AllowAny,)
  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({"status": True, "message": "User created Successfully"}, status=status.HTTP_201_CREATED)

class LogoutAPIView(APIView):
  permission_classes = (permissions.IsAuthenticated,)
  def post(self, request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ResetPasswordRequestView(APIView):
  def post(self, request):
    serializer = ResetPasswordRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    user = User.objects.filter(email=email)
    if not user.exists(): return Response({"status": False, "message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    token_obj = PasswordResetToken.objects.create(user=user, expires_at=timezone.now() + timedelta(minutes=10))
    return Response({"status": True, "message": "Reset token generated", "token": str(token_obj.token)}, status=status.HTTP_200_OK)

class ResetPasswordConfirmView(APIView):
  def post(self, request):
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    token_obj = PasswordResetToken.objects.filter(token=data["token"])

    if not token_obj.exists(): return Response({"status": False, "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    token_obj = token_obj.first()
    if token_obj.is_used or token_obj.is_expired(): return Response({"status": False, "message": "Token expired or used"}, status=status.HTTP_400_BAD_REQUEST)
    user = token_obj.user
    user.set_password(data["new_password"])
    user.save()
    token_obj.is_used = True
    token_obj.save()
    return Response({"status": True, "message": "Password reset successfully"})
