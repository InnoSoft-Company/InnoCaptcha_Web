from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import UserSerializer

User = get_user_model()

class LoginView(APIView): 
  def post(self, request):
    data = UserSerializer(request.user)
    data.is_valid()
    data = data.data

class RegisterView(APIView):
  def post(self, request):
    data = UserSerializer(request.user)
    data.is_valid()
    data = data.data
    user = User.objects.create_user(**data)
