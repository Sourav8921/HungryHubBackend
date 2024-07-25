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
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

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


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(default="default.jpg", upload_to="category_images")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default="default.jpg", upload_to="dishes_pics")

    class Meta:
        indexes = [models.Index(fields=["name"])]

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
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Prepared', 'Prepared'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=16,
        choices=ORDER_STATUS_CHOICES,
        default='Pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
