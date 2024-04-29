from django.db import models


class Restaurants(models.Model):
    name = models.CharField(max_length=255)
    delivery_time = models.IntegerField()
    cuisine_type = models.CharField(max_length=50)
    place = models.CharField(max_length=20)
    image_url = models.CharField(max_length=2083)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=2083)

    def __str__(self):
        return self.name


