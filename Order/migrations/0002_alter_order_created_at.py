# Generated by Django 4.1.7 on 2023-05-28 16:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 28, 16, 47, 28, 368474, tzinfo=datetime.timezone.utc)),
        ),
    ]
