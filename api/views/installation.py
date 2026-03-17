from django.http import HttpResponse
from django.views import View
from django.conf import settings
import os

class DatabaseDownloadView(View):
  def get(self, request):
    db_path = os.path.join(settings.BASE_DIR, 'core/dbs/captcha.db')
    with open(db_path, 'rb') as db_file:
      response = HttpResponse(db_file.read(), content_type='application/octet-stream')
      response['Content-Disposition'] = 'attachment; filename="captcha.db"'
      return response