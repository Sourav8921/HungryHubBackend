import os

from django.db import models
from PIL import Image
from users.models import CustomUser


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    delivery_time = models.PositiveIntegerField()
    cuisine_type = models.CharField(max_length=50)
    place = models.CharField(max_length=20)
    image = models.ImageField(default="default.jpg", upload_to="restaurant_pics")

    def __str__(self):
        return self.name

    # function to resize upload image if it exceeds 600px
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the image field is not empty and the file exists
        if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default="default.jpg", upload_to="dishes_pics")

    def __str__(self):
        return self.name

    # function to resize upload image if it exceeds 600px
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the image field is not empty and the file exists
        if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
