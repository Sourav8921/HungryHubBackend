# Generated by Django 5.0.4 on 2024-05-16 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_remove_menuitem_image_url_menuitem_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Restaurants',
            new_name='Restaurant',
        ),
    ]