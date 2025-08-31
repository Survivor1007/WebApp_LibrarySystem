from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Book, Borrow
from .serializers import BookSerializers, BorrowSerializers, UserRegisterSerializer


class BookViewSet(viewsets.ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializers
      permission_classes = [IsAuthenticated]


      @action(detail = False, methods = ['post'], url_path = "donate")
      def donate_book(self, request):
            title = request.data.get("title")
            author = request.data.get("author")
            copies = int(request.data.get("copies", 1))

            if not title or not author :
                  return Response(
                        {"error" : "Detiails insufficiuent"},
                        status = status.HTTP_400_BAD_REQUEST
                        )
            

            book, created = Book.objects.get_or_create(
                  title = title,
                  author = author,
                  defaults= {"available_copies" : copies}
            )

            if not created:
                  book.available_copies += copies
                  book.save()
            
            return Response(
                  {"message" : f"{request.user.username} has donated {book.title}.Thanks for your valuable contribution"},
                  status = status.HTTP_201_CREATED
            )

class BorrowViewSet(viewsets.ModelViewSet):
      queryset = Borrow.objects.all()
      serializer_class = BorrowSerializers
      permission_classes = [IsAuthenticated]

      def create(self, request, *args, **kwargs):
            book_id = request.data.get("book")
            try :
                  book = Book.objects.get(id = book_id)
            except Book.DoesNotExist:
                  return Response({"error" : "Couldn't find book"}, status = status.HTTP_404_NOT_FOUND)
            
            if book.available_copies < 1:
                  return Response({"error" : "No available copies"}, status = status.HTTP_400_BAD_REQUEST)
            
            borrow = Borrow.objects.create(
                  user = request.user,
                  book = book
            )

            book.available_copies -= 1
            book.save()

            serializer = self.get_serializer(borrow)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
      
      @action(detail = True, methods = ["post"], url_path = "return")
      def return_book(self,request, pk = None):
            try:
                  borrow = self.get_object()
            except Borrow.DoesNotExist:
                  return Response({"error" : "Borrow Record not found"}, status = status.HTTP_404_NOT_FOUND)
            
            book = borrow.book

            borrow.delete()

            book.available_copies += 1
            book.save()

            return Response({"message" : f"{book.title} is returned successfully by {borrow.user.username}"}, status = status.HTTP_200_OK)

            

class RegisterView(generics.CreateAPIView):
      queryset = User.objects.all()
      serializer_class = UserRegisterSerializer
      permission_classes = [AllowAny]

      def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Create the user

        # generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access),
            },
            status=status.HTTP_201_CREATED,
        )

