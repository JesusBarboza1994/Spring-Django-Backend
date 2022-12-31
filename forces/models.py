from django.db import models
from django.contrib.postgres.fields import ArrayField

from spring.models import Spring

class Forces(models.Model):
  forces = ArrayField(models.DecimalField(max_digits=5, decimal_places=1), default=list())
  displacements = ArrayField(models.DecimalField(max_digits=5, decimal_places=1), default=list())
  spring = models.ForeignKey(Spring, on_delete=models.CASCADE, default="0")

