from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Book(models.Model):
      title = models.CharField(max_length=200)
      author = models.CharField(max_length=200)
      isbn = models.CharField(max_length=13)
      available_copies = models.IntegerField(default = 1)
      def __str__(self):
            return self.title
      
class Borrow(models.Model):
      user  = models.ForeignKey(User, on_delete=models.CASCADE)
      book = models.ForeignKey('Book', on_delete=models.CASCADE)
      borrow_at = models.DateTimeField(auto_now_add=True)
      return_on = models.DateTimeField(blank = True, null = True)

      def __str__(self):
            return f"{self.user.username} borrowed the book {self.book.title}"