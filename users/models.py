from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username


class DeliveryAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255, default='Default Street Address')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_label = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code}"
