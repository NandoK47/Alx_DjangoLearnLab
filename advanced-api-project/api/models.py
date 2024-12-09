from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    publication_year = models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.title} ({self.publication_year})"

class MyModel(models.Model):
    my_date_field = models.DateField(default=timezone.now)
    