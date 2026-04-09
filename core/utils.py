from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from .MainVariables import EmailConfig
import hashlib, secrets, requests, re
from django.shortcuts import render

def generate_secure_token(): 
  token = secrets.token_urlsafe(32)
  hashed = hashlib.sha256(token.encode()).hexdigest()
  return token, hashed

def redirectToNext(request, to='/'):
  if isinstance(to, HttpResponseRedirect):
    to = to.url
  if not isinstance(to, str):
    to = '/'
  match = re.search(r'(/.*)', to)
  safe_to = match.group(1) if match else '/'
  return render(request, 'utils/redirect.html', {'to': safe_to})

class SMTP2GOClient:
  def __init__(self, api_key=EmailConfig['API_KEY'], base_url=EmailConfig['API_URL'], timeout=10):
    self.api_key = api_key
    self.base_url = base_url
    self.timeout = timeout

  def send(self, *, sender=None, to=None, subject=None, text_body=None, html_body=None, cc=None, bcc=None, custom_headers=None, attachments=None, inlines=None, template_id=None, template_data=None, extra_payload=None):
    if not sender: raise ValueError("sender is required")
    if not to: raise ValueError("to is required")
    if not subject and not template_id: raise ValueError("subject is required unless using template_id")
    if isinstance(to, str): to = [to]
    payload = {
      "sender": sender,
      "to": to,
      "subject": subject,
      "text_body": text_body,
      "html_body": html_body,
      "cc": cc,
      "bcc": bcc,
      "custom_headers": custom_headers,
      "attachments": attachments,
      "inlines": inlines,
      "template_id": template_id,
      "template_data": template_data
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    if extra_payload: payload.update(extra_payload)
    try:
      response = requests.post(self.base_url, json=payload, headers={"Content-Type": "application/json", "accept": "application/json", "X-Smtp2go-Api-Key": self.api_key}, timeout=self.timeout)
      data = response.json() or response.text
      return {"status": True, "status_code": response.status_code, "data": data} if response.status_code == 200 else {"status": False, "status_code": response.status_code, "error": data}
    except requests.exceptions.Timeout: return {"status": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e: return {"status": False, "error": str(e)}
