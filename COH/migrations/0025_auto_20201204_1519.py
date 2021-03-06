# Generated by Django 3.1.3 on 2020-12-04 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COH', '0024_auto_20201204_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo_file',
            field=models.ImageField(default='photos/default.jpg', upload_to='photos'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo_name',
            field=models.CharField(default='default.jpg', max_length=64),
        ),
    ]
