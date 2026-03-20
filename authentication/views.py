from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ResetPasswordRequestSerializer
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
OTP_EXPIRY_SECONDS = 300

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
