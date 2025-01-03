from django.shortcuts import render
from rest_framework import generics, permissions
from django_filters import rest_framework
from .models import Book
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.

class BookListView(generics.ListAPIView):
     queryset = Book.objects.all()
     serializer_class = BookSerializer
     filter_backends = [DjangoFilterBackend, 'filters.OrderingFilter', 'filters.SearchFilter']
     filter_fields = ['title', 'author_name', 'publication_year']
     search_fields = ['title', 'author_name']
     ordering_fields = ['title', 'author_name']
     
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
     
class BookTests(APITestCase):
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        url = '/api/books/'
        data = {'title': 'Test Book', 'published_date': '2024-01-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['published_date'], '2024-01-01')
        
        def test_create_book_unauthenticated(self):
        # Make the POST request without logging in
        
         url = '/api/books/'
        data = {'title': 'Test Book', 'published_date': '2024-01-01'}
        
        response = self.client.post(url, data, format='json')
        
        # Check that authentication is required (e.g., HTTP 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)