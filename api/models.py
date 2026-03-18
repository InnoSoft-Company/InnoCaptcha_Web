from django.db import models
import uuid

class ReposVisitors(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self): return f"Visit id: {self.id} created at: {self.created_at}"

class InstallPayload(models.Model):
    package = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    python_version = models.CharField(max_length=20, blank=True, null=True)
    python_impl = models.CharField(max_length=20, blank=True, null=True)
    os = models.CharField(max_length=50, blank=True, null=True)
    os_release = models.CharField(max_length=50, blank=True, null=True)
    architecture = models.CharField(max_length=50, blank=True, null=True)
    processor = models.CharField(max_length=100, blank=True, null=True)
    hostname = models.CharField(max_length=100, blank=True, null=True)
    cpu_count = models.IntegerField(blank=True, null=True)
    cwd = models.CharField(max_length=300, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.package} v{self.version} ({self.created_at.date()})"

class CaptchaInstallAnalytics(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self): return f"Download id: {self.id} @ {self.created_at}"
