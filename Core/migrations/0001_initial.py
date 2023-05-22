# Generated by Django 4.1.7 on 2023-05-22 09:37

import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sizes_available', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('manufacturer', models.CharField(max_length=100)),
                ('default_img', models.FileField(upload_to='media/default')),
                ('category', models.CharField(choices=[('K', 'Kids'), ('M', 'Men'), ('W', 'Women')], max_length=255)),
                ('slug', models.SlugField(blank=True)),
                ('availability_status', models.CharField(choices=[('A', 'Available'), ('U', 'Unavailable'), ('R', 'Restocked')], max_length=24)),
                ('date_added', models.DateTimeField(default=datetime.datetime(2023, 5, 22, 10, 37, 10, 718326))),
                ('newly_added', models.BooleanField(default=True)),
                ('rating', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Boots',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField()),
                ('text', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.boots')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='BootsVariants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_available', models.IntegerField()),
                ('color', models.CharField(max_length=23)),
                ('image_1', models.FileField(upload_to='media')),
                ('image_2', models.FileField(blank=True, upload_to='media')),
                ('image_3', models.FileField(blank=True, upload_to='media')),
                ('boot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.boots')),
            ],
            options={
                'verbose_name_plural': 'Boots Variants',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=355)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
