# Generated by Django 3.1.3 on 2020-12-04 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('COH', '0019_auto_20201204_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='photo_file',
        ),
        migrations.RemoveField(
            model_name='user',
            name='photo_name',
        ),
    ]
