# Generated by Django 3.1.3 on 2020-12-29 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COH', '0025_auto_20201204_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='overtime',
            name='month',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
