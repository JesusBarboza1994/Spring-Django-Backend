from django.db import models
from django.contrib.postgres.fields import ArrayField

from spring.models import Spring

# Create your models here.
class Points(models.Model):
  posx = ArrayField(models.DecimalField(max_digits=5, decimal_places=1), default=list())
  posy = ArrayField(models.DecimalField(max_digits=5, decimal_places=1), default=list())
  posz = ArrayField(models.DecimalField(max_digits=5, decimal_places=1), default=list())
  esf = ArrayField(models.DecimalField(max_digits=5, decimal_places=1), default=list())
  spring = models.ForeignKey(Spring, on_delete=models.CASCADE, default="0")