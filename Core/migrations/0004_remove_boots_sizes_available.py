# Generated by Django 4.1.7 on 2023-06-18 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_boots_last_modified_reviews_date_added_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boots',
            name='sizes_available',
        ),
    ]