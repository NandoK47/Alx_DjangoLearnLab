# Generated by Django 5.1.3 on 2024-12-07 21:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_book_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 7, 21, 18, 34, 645521, tzinfo=datetime.timezone.utc)),
        ),
    ]