from .serializers import LoginSerializer, RegisterationSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model()

class LoginView(APIView): 
  def post(self, request):
    data = LoginSerializer(request.data)
    data.is_valid()
    data = data.data

class RegisterView(APIView):
  def post(self, request):
    data = RegisterationSerializer(request.data)
    data.is_valid()
    data = data.data
    user = User.objects.create_user(**data)
