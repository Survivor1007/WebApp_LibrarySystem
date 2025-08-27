from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from .models import Book, Borrow
from .serializers import BookSerializers, BorrowSerializers


class BookViewSet(viewsets.ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializers


class BorrowViewSet(viewsets.ModelViewSet):
      queryset = Borrow.objects.all()
      serializer_class = BorrowSerializers


