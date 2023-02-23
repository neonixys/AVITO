# Generated by Django 4.0.1 on 2023-02-22 06:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default=1, max_length=10, validators=[django.core.validators.MinLengthValidator(5)]),
            preserve_default=False,
        ),
    ]
