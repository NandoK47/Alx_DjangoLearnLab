from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework
from rest_framework.generics import ListAPIView

# Create your views here.

class BookListView(generics.ListAPIView):
     queryset = Book.objects.all()
     serializer_class = BookSerializer
     filter_backends = [DjangoFilterBackend, OrderingFilter]
     filter_fields = ['title', 'author_name', 'publication_year']
     search_fields = ['title', 'author_name']
     ordering_fields = ['title', 'publication_year']
     
class BookDetailView(generics.RetrieveAPIView):
     queryset = Book.objects.all()
     serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
     queryset = Book.objects.all()
     serializer_class = BookSerializer
     permission_classes = [permissions.IsAuthenticated]
     def perform_create(self, serializer):
           if serializer.validated_data['publication_year'] > 2024:
            raise ValidationError("Publication year cannot be in the future.")
           serializer.save(author=self.request.user)

class BookUpdateView(generics.UpdateAPIView):
     queryset = Book.objects.all()
     serializer_class = BookSerializer
     permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
     queryset = Book.objects.all()
     serializer_class = BookSerializer
     permission_classes = [permissions.IsAuthenticated]

class IsAdminOrReadOnly(BasePermission):
     def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff