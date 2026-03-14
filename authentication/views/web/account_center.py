from django.views.decorators.http import require_http_methods, require_GET
from core.utils.useragent import get_user_agent, get_client_ip
from core.utils.sendemail import send_verification_code_async
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse
import random, pytz

@require_GET
def myProfile(request):
  return render(request, "auth/account_center/myProfile.html")

@require_http_methods(["GET", "POST"])
def activateAccount(request):
  if request.user.verified: return redirect(reverse("web-home"))
  session = request.session
  def set_activation_session(code): session["activateCode"], session["activateCodeTime"], session["activateTries"] = str(code), now().isoformat(), 0
  def send_activation_email(code): send_verification_code_async(subject=f"Verify Email: {request.user.email}", receiver_email=request.user.email, code=code, from_email="verify@accountcenter.auth.authflowx.midoghanam.site", from_name="AuthFlowX - Verify Email", request=request)
  if request.method == "GET":
    code = random.randint(100000, 999999)
    set_activation_session(code)
    send_activation_email(code)
    return render(request, "auth/account_center/activate.html")
  verification_code = request.POST.get("verification_code", "").strip()
  saved_code = session.get("activateCode")
  code_time = session.get("activateCodeTime")
  tries = session.get("activateTries", 0)
  if not verification_code or not verification_code.isdigit():
    messages.error(request, "Invalid verification code.")
    return render(request, "auth/account_center/activate.html")
  if not saved_code or not code_time:
    messages.error(request, "Code expired. A new one has been sent.")
    code = random.randint(100000, 999999)
    set_activation_session(code)
    send_activation_email(code)
    return render(request, "auth/account_center/activate.html")
  if now() > datetime.fromisoformat(code_time) + timedelta(minutes=10):
    messages.error(request, "Code expired. A new one has been sent.")
    code = random.randint(100000, 999999)
    set_activation_session(code)
    send_activation_email(code)
    return render(request, "auth/account_center/activate.html")
  if tries >= 5:
    messages.error(request, "Too many attempts.")
    return render(request, "auth/account_center/activate.html")
  if verification_code != saved_code:
    session["activateTries"] = tries + 1
    messages.error(request, "Wrong verification code.")
    return render(request, "auth/account_center/activate.html")
  for key in ["activateCode", "activateCodeTime", "activateTries"]: session.pop(key, None)
  request.user.verified = True
  request.user.save()
  messages.success(request, "Account activated successfully.")
  return redirect(reverse("web-home"))
