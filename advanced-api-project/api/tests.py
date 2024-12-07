from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Author
from django.contrib.auth.models import User

# Create your tests here.

class TestBookAPI(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')
        self.book_url = '/api/books/' 

        self.author1 = Author.objects.create(name='Author A')
        self.author2 = Author.objects.create(name='Author B')

        self.book1 = Book.objects.create(title='Book One', author=self.author1, published_date='2023-01-01')
        self.book2 = Book.objects.create(title='Book Two', author=self.author2, published_date='2023-02-01')

    def test_create_book(self):
        data = {'title': 'New Book', 'author': 'self.author1.id', 'published_date': '2024-01-01'}
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['author'], self.author1.id)

    def test_get_books(self):
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_book(self):
        update_url = f'{self.book_url}{self.book1.id}/'
        data = {'title': 'Updated Book', 'author': 'Author A'}
        response = self.client.put(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')
    
    def test_filter_books_by_author(self):
        response = self.client.get(f'{self.book_url}?author=Author A')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.id)

    def test_order_books_by_title(self):
        response = self.client.get(f'{self.book_url}?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book One')
