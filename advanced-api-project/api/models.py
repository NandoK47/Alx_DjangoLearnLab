from django.db import models
from django.utils import timezone
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    published_date = models.DateField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

class MyModel(models.Model):
    my_date_field = models.DateField(default=timezone.now)
    