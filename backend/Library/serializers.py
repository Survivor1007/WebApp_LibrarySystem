from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Borrow

class BookSerializers(serializers.ModelSerializer):
      class Meta:
            model = Book
            fields = '__all__'


class BorrowSerializers(serializers.ModelSerializer):
      class Meta:
            model = Borrow
            fields = '__all__'

      
class UserRegisterSerializer(serializers.ModelSerializer):
      password = serializers.CharField(min_length = 8, write_only = True)

      class Meta:
            model = User
            fields = ['username', 'email', 'password']

      def create(self, validate_data):
            user = User.objects.create_user(
                  username=validate_data['username'],
                  email=validate_data.get('email'),
                  password=validate_data['password']
            )

            return user