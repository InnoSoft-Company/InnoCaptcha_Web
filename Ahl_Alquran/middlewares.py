from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response
  def __call__(self, request):
    if request.user.is_authenticated:
      auth_paths = [reverse('auth-login'), reverse('auth-register')]
      if request.path in auth_paths: return redirect('/')
    return self.get_response(request)
