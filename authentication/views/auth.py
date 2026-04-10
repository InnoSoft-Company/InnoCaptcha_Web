from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from core.utils import redirectToNext
from django.contrib import messages
from .. import models as m

User = get_user_model()

def login(request):
  if request.method == "POST":
    identity = request.POST.get('identity')
    password = request.POST.get('password')
    user_obj = None
    if identity:
      user_obj = User.objects.filter(username=identity).first()
      if not user_obj: user_obj = User.objects.filter(email=identity).first()
      if not user_obj: user_obj = User.objects.filter(phone=identity).first()
    if user_obj: user = authenticate(request, username=user_obj.username, password=password)
    else: user = None
    if user is not None:
      auth_login(request, user)
      nextSaved = request.session.get("next", "")
      return redirectToNext(request=request, to=nextSaved if nextSaved else redirect('dashboard'))
    else:
      messages.error(request, "بيانات الدخول غير صحيحة")
      return redirect('auth-login')
    request.session["next"] = request.GET.get("next", "")
  return render(request, 'auth/login.html')

def register(request):
  if request.method == "POST":
    username = request.POST.get('full_name') or request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    id_image = request.FILES.get('id_image')
    
    if not id_image:
      messages.error(request, "يجب إرفاق صورة الهوية أو شهادة الميلاد")
      return redirect('auth-register')
      
    if password != request.POST.get('password_confirm'):
      messages.error(request, "الباسورد غير مطابق")
      return redirect('auth-register')
    if User.objects.filter(username=username).exists():
      messages.error(request, "الاسم مستخدم من قبل, اختر اسماً آخر")
      return redirect('auth-register')
    if User.objects.filter(email=email).exists():
      messages.error(request, "البريد الإلكتروني مسجل بالفعل")
      return redirect('auth-register')
    if phone and User.objects.filter(phone=phone).exists():
      messages.error(request, "رقم الهاتف مسجل بالفعل")
      return redirect('auth-register')
      
    user = User.objects.create_user(username=username, email=email, phone=phone, password=password)
    user.id_image = id_image
    user.save()
    messages.success(request, "تم انشاء الحساب بنجاح")
    return redirect('auth-login')
  return render(request, 'auth/register.html')

def logout(request):
  auth_logout(request)
  return redirect('/')
