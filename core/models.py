from django.db import models
import uuid

class Release(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  version = models.CharField(max_length=50,unique=True)
  source_url = models.URLField()
  wheel_url = models.URLField()
  notes = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  class Meta: ordering = ["-created_at"]
  def __str__(self): return f"{self.version} established @ {self.created_at}"
