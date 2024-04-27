from django.db import models


class Restaurants(models.Model):
    name = models.CharField(max_length=255)
    delivery_time = models.IntegerField()
    cuisine_type = models.CharField(max_length=50)
    place = models.CharField(max_length=20)
    image_url = models.CharField(max_length=2083)




