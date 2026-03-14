from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status, permissions

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_username(request): return Response({"status": True, "exists": True if User.objects.filter(username=request.GET.get("username", "")).exists() else False})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_email(request): return Response({"status": True, "exists": True if User.objects.filter(email=request.GET.get("email", "")).exists() else False})

