from django.db import models
from django.db.models import ForeignKey

# Create your models here.



class Crag(models.Model):
    start_point_jp = models.CharField(max_length=256)
    input_distance_km = models.IntegerField()