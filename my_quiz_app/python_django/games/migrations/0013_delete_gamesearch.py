# Generated by Django 5.0.7 on 2024-08-07 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0012_gamerandom_points_updated'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GameSearch',
        ),
    ]