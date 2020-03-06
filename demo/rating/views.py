from django.shortcuts import render
from rating.models import User
from rating.serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView

class UsersAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


