# Generated by Django 5.1.3 on 2024-12-07 21:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_book_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]