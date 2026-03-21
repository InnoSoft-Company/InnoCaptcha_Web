from django.contrib import admin
from .models import *

admin.site.site_header = "Competition Admin"
admin.site.site_title = "Competition Admin Portal"

admin.site.register(Competition)
admin.site.register(Participants)
