# Generated by Django 3.2.12 on 2022-04-08 20:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='review_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]