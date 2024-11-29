from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Article
from .models import Book
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.

def secure_view(request):
    response = HttpResponse("<h1>Secure Content</h1>")
    response['Content-Security-Policy'] = "default-src 'self'; script-src 'self';"
    return response

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# View to add a new book (requires permission)
@permission_required('bookshelf.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = 'BookForm'(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = 'BookForm'()
    return render(request, 'add_book.html', {'form': form})

# View to edit an existing book (requires permission)
@permission_required('bookshelf.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = 'BookForm'(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = 'BookForm'(instance=book)
    return render(request, 'edit_book.html', {'form': form})

# View to delete a book (requires permission)
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})

# Safe, parameterized query using Django ORM
book = Book.objects.filter(Q(title__icontains='user_input'))