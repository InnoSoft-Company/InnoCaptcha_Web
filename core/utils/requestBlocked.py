from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
import uuid

def blocked_request(request, block_type=None):
    context = {
        "block_type": block_type,  # "spam", "security", "rate_limit", "maintenance"
        "error_message": "Your request has been flagged as potential spam activity.",
        "block_reason": "Multiple failed login attempts detected",
        "request_id": "REQ_" + str(uuid.uuid4())[:8],
        "ip_address": request.META.get('REMOTE_ADDR'),
        "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "block_duration": "15 minutes",
        "retry_after": 30,  # seconds for rate limit
        "server_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "urls": {
            "index": reverse("index"),
            "login": reverse("web-auth-login"),
        }
    }
    return render(request, "ERROR/BlockedRequest.html", context, status=423)