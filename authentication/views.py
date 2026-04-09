from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from core.utils import redirectToNext
from django.contrib import messages
from . import models as m

def login(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      auth_login(request, user)
      nextSaved = request.session.get("next", "")
      return redirectToNext(request=request, to=nextSaved if nextSaved else redirect('home'))
    else:
      messages.error(request, "Invalid username or password")
      return redirect('login')
    request.session["next"] = request.GET.get("next", "")
  return render(request, 'auth/login.html')

def register(request):
  if request.method == "POST":
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    if password != password2:
      messages.error(request, "الباسورد غير مطابق")
      return redirect('auth-register')
    if User.objects.filter(username=username).exists():
      messages.error(request, "اسم المستخدم مكرر, استخدم اخر")
      return redirect('auth-register')
    if User.objects.filter(email=email).exists():
      messages.error(request, "الباسورد مسجل من قبل, استخدم اخر")
      return redirect('auth-register')
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    messages.success(request, "تم انشاء الحساب بنجاح")
    return redirect('auth-login')
  return render(request, 'auth/register.html')

def logout(request):
  auth_logout(request)
  return redirect('/')
