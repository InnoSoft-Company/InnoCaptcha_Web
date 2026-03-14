from core.utils.useragent import get_user_agent, get_client_ip
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from core.MainVariables import BaseURL
from django.conf import settings
from django.urls import reverse
from datetime import datetime
import threading

def send_verification_code(subject, receiver_email, code, from_email, from_name, request, reply_to=None):
  try:
    html_content = render_to_string("emails/activate-account.html", { "code": code, "user": request.user, "activate_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ip": get_client_ip(request), "user_agent": f"{get_user_agent(request)['device_type']} - {get_user_agent(request)['os']} - {get_user_agent(request)['browser']}", "BaseURL": BaseURL, "website_url": BaseURL + "/",})
    email = EmailMultiAlternatives(subject=subject, body=html_content, from_email=f"{from_name} <{from_email}>", to=[receiver_email], reply_to=[reply_to or from_email],)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return {"success": True}
  except Exception as e:
    return {"success": False, "error": str(e)}
  
def send_verification_code_async(*args, **kwargs):
  thread = threading.Thread(target=send_verification_code, args=args, kwargs=kwargs)
  thread.daemon = True
  thread.start()
