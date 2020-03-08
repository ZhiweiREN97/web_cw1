from django.shortcuts import render
from rating.models import User, userToken
from rating.serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView
from django.http import JsonResponse
from rest_framework.views import APIView
import time

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rating.permissions import IsOwnerOrReadOnly


class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        print (username)
        password = data.get('password')
        user = User.objects.get(username=username)
        if self.request.session['user_id'] is not None:
            return Response({"message":"You have already logged in!"},status=HTTP_400_BAD_REQUEST)
            
        if user.password == password:
            serializer = UserSerializer(user)
            new_data = serializer.data
            # logged in user
            self.request.session['user_id'] = user.u_id
            return Response(new_data, status=HTTP_200_OK)
        return Response('password error', HTTP_400_BAD_REQUEST)

class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data
        if User.objects.filter(username__exact=username):
            return Response("Username exists",HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, requests, format=None):
        if self.request.session['user_id'] is not None:
            self.request.session['user_id'] = None
            return Response({"message":"Logout Success"},status=HTTP_200_OK)
        else:
            return Response({"message":"You have not logged in yet"},status=HTTP_400_BAD_REQUEST)


class UsersAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class AuthView(APIView):

    def post(self,request,*args,**kwargs):
        ret = {'code':1000,'msg':None}
        try:
            usr = request.data.get('username')
            pas = request.data.get('password')
            obj = User.objects.filter(username=usr,password=pas).first()
            if not obj:
                ret['code'] = '1001'
                ret['msg'] = 'Username or password error'
                return JsonResponse(ret)
            token = str(time.time()) + usr
            userToken.objects.update_or_create(username=obj, defaults={'token': token})
            ret['msg'] = 'Login Success!'
            #ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = 'Request error'
        return JsonResponse(ret)

