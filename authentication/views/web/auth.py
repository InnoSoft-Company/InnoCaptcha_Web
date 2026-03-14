from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

User = get_user_model()

@require_http_methods(["GET", "POST"])
def login(request):
  if request.method == "POST":
    email, username, password = request.POST.get("email"), request.POST.get("username").lower(), request.POST.get("password")
    user = None
    if email:
      try: user = authenticate(request, username=User.objects.get(email=email).username, password=password)
      except User.DoesNotExist: user = None
    elif username: user = authenticate(request, username=username, password=password)
    if user is not None:
      auth_login(request, user)
      return redirect(reverse("web-home"))
    else: messages.error(request, "Invalid credentials")
  context = {
    "urls": {
      "index": reverse("index"),
      "signup": reverse("web-auth-signup"),
      "forgotPassword": reverse("web-auth-forgotPassword"),
      "OAuth": {
        "google": reverse("web-auth-oauth-redirect", kwargs={"oauth_provider": "google"}) + f"?action=login&redirect={reverse('web-home')}",
        "github": reverse("web-auth-oauth-redirect", kwargs={"oauth_provider": "github"}) + f"?action=login&redirect={reverse('web-home')}",
      },
    },
  }
  return render(request, "auth/login.html", context)

@require_http_methods(["GET", "POST"])
def signup(request):
  if request.method == "POST":
    username, email, password, password_confirm = request.POST.get("username"), request.POST.get("email"), request.POST.get("password"), request.POST.get("password_confirm")
    if password != password_confirm: messages.error(request, "Passwords do not match")
    elif User.objects.filter(username=username).exists(): messages.error(request, "Username already taken")
    elif User.objects.filter(email=email).exists(): messages.error(request, "Email already registered")
    else:
      user = User.objects.create_user(username=username, email=email, password=password)
      messages.success(request, f"Account is created.. Please login")
      return redirect(reverse("web-auth-login"))
  context = {
    "urls": {
      "index": reverse("index"),
      "login": reverse("web-auth-login"),
      "apis": {
        "check_username": reverse("api-auth-check_username"),
        "check_email": reverse("api-auth-check_email"),
      },
      "OAuth": {
        "google": reverse("web-auth-oauth-redirect", kwargs={"oauth_provider": "google"}) + f"?action=signup&redirect={reverse('web-home')}",
        "github": reverse("web-auth-oauth-redirect", kwargs={"oauth_provider": "github"}) + f"?action=signup&redirect={reverse('web-home')}",
      },
    },
  }
  return render(request, "auth/signup.html", context)

@require_GET
@login_required
def logout(request):
  auth_logout(request)
  return redirect(reverse("web-auth-login"))
