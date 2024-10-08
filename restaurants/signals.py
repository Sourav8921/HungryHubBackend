import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Restaurant, MenuItem, Category


# whenever a Restaurant or MenuItem object is deleted, the corresponding image file
# associated with it will be deleted from the media folder as well.
@receiver(post_delete, sender=Restaurant)
@receiver(post_delete, sender=MenuItem)
@receiver(post_delete, sender=Category)
def delete_related_images(sender, instance, **kwargs):
    if hasattr(instance, 'image') and instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)

