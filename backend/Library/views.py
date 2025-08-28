from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Book, Borrow
from .serializers import BookSerializers, BorrowSerializers, UserRegisterSerializer


class BookViewSet(viewsets.ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializers
      permission_classes = [IsAuthenticated]


class BorrowViewSet(viewsets.ModelViewSet):
      queryset = Borrow.objects.all()
      serializer_class = BorrowSerializers
      permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
      queryset = User.objects.all()
      serializer_class = UserRegisterSerializer
      permission_classes = [AllowAny]



