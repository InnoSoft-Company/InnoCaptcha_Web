from rest_framework import serializers
from .models import InstallPayload

class InstallPayloadSerializer(serializers.ModelSerializer):
  class Meta:
    model = InstallPayload
    fields = "__all__"
