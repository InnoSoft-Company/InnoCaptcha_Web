from django.db import models

class Competition(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  def __str__(self): return self.name

class Participants(models.Model):
  name = models.CharField(max_length=255)
  competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

  score = models.FloatField(default=0.0)
  def __str__(self): return f"{self.name} @ {self.competition.name} with score {self.score}"


