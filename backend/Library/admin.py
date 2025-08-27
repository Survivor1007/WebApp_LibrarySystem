from django.contrib import admin
from .models import Book, Borrow
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
      list_display = ( 'title' , 'author', 'isbn', 'available_copies')
      search_fields = ('title', 'author')

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
      list_display = ('user', 'book', 'borrow_at', 'return_on')
      search_fields = ('book',)
