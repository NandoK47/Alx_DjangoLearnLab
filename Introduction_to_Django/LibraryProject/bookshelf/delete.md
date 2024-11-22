from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by checking if any books exist
books = Book.objects.all()
print(books)
# Output: <QuerySet []>
