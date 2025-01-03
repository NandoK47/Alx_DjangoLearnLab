from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm
# Create your views here.

def list_books(request):
    books = Book.objects.all()  
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  
    context_object_name = 'library'

# User Login View
class LoginView(View):
    def get(self, request):
        form = 'AuthenticationForm'()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = 'AuthenticationForm'(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect URL
        return render(request, 'login.html', {'form': form})

# User Logout View
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'logout.html')

# User Registration View
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect URL
        return render(request, 'register.html', {'form': form})
    
# Role check functions
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'
@user_passes_test(is_admin, login_url='/login/')  # Redirect unauthorized users to login
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})

def is_librarian(user):
     return user.is_authenticated and user.userprofile.role == 'Librarian'
@user_passes_test(is_librarian, login_url='/login/')  # Redirect unauthorized users to login
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})


def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'
@user_passes_test(is_member, login_url='/login/')  # Redirect unauthorized users to login
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'user': request.user})


# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html')

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')

# View to add a book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to a list of books
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

# View to edit a book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

# View to delete a book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})