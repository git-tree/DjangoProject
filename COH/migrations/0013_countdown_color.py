# Generated by Django 3.1.3 on 2020-11-27 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COH', '0012_remove_countdown_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='countdown',
            name='color',
            field=models.CharField(default='#1E9FFF', max_length=20),
        ),
    ]