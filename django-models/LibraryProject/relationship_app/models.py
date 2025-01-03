from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
class Meta:
        permissions = [
            ("can_add_book", "Can add a new book"),
            ("can_change_book", "Can edit an existing book"),
            ("can_delete_book", "Can delete a book"),
        ]
        def __str__(self):
             return self.title

class Library(models.Model):
    name = models.CharField(max_length=150)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    
    
# Define roles

ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')  # Role field

    def __str__(self):
        return f"{self.user.username} - {self.role}"    
    
# Automatically create or update UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()    