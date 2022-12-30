from django.db import models
from django.contrib.postgres.fields import ArrayField

from spring.models import Spring

# Create your models here.
class Points(models.Model):
  x = ArrayField(models.DecimalField(max_digits=5, decimal_places=1))
  y = ArrayField(models.DecimalField(max_digits=5, decimal_places=1))
  z = ArrayField(models.DecimalField(max_digits=5, decimal_places=1))
  # x = models.DecimalField(max_digits=5, decimal_places=1)
  # y = models.DecimalField(max_digits=5, decimal_places=1)
  # z = models.DecimalField(max_digits=5, decimal_places=1)
  spring = models.ForeignKey(Spring, on_delete=models.CASCADE, default="0")