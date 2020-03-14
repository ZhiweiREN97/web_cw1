from django.shortcuts import render
from rating.models import User, userToken, Score, Professor, Module
from rating.serializers import *
from rest_framework.generics import ListCreateAPIView, ListAPIView
from django.http import JsonResponse
from rest_framework.views import APIView
import time

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rating.permissions import IsOwnerOrReadOnly

#Login
class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        user = User.objects.get(username=username)

        if user.password == password:
            serializer = UserSerializer(user)
            new_data = serializer.data            
            self.request.session['user_id'] = user.id
            print (self.request.session['user_id'])
            return Response('Login successful!', status=HTTP_200_OK)
        return Response('Password error', HTTP_400_BAD_REQUEST)

#Register
class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        if User.objects.filter(username__exact=username):
            return Response("Username exists",HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Register Sucessful!',status=HTTP_200_OK)
        return Response("Register error", status=HTTP_400_BAD_REQUEST)

#Logout
class LogoutAPIView(APIView):
    def post(self, requests, format=None):
        # if session['user_id'] does not exists
        if self.request.session.get('user_id',None) is None:
            return Response({"message":"You have not logged in yet!"},status=HTTP_400_BAD_REQUEST)
        elif self.request.session['user_id'] is not None:
            self.request.session['user_id'] = None
            return Response("Logout Success",status=HTTP_200_OK)
        else:
            return Response("You have not logged in yet",status=HTTP_400_BAD_REQUEST)

#List All user
class UsersAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

#List a user
class UserAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

#List all modules
class ModuleAPIView(ListAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()

#Avg of one module one professor
class AvgAPIView(APIView):
    serializer_class = AvgSerializer
    queryset = Score.objects.all()

    def post(self, request, format=None):
        data = request.data
        p_id = data.get('p_id')
        module_id = data.get('module_id')
        prof = Professor.objects.get(p_id=p_id)
        module = Module.objects.get(module_id=module_id)
        avg = 0
        count = 0
        scoreset = Score.objects.filter(professor = prof, module= module)
        for i in scoreset:
            avg += i.score
            count += 1
        avg = avg /count
        message = "The rating of Professor %s (%s) in module %s (%s) is %f ;" %(prof.lastname, prof.p_id, module.module_name, module.module_id,avg)
        return Response(message,status=HTTP_200_OK)

#Rating of all professors
class AllRatingAPIView(ListAPIView):
    def post(self, request, format=None):
        profset = Professor.objects.all()
        message = ""
        for i in profset:
            avg_rating = 0
            count = 0
            scoreset = Score.objects.filter(professor = i)
            for j in scoreset:
                avg_rating += j.score
                count += 1
            if count !=0:
                avg_rating = avg_rating / count
            message = message + "The rating of professor %s (%s) is %f ;" %(i.lastname, i.p_id, avg_rating) 
        return Response(message,status=HTTP_200_OK)






class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        try:
            prof_id = self.request.data.get("professor")
            m_id = self.request.data.get("module")
            prof = Professor.objects.get(p_id=prof_id)
            module = Module.objects.get(module_id=m_id,prof = prof)
            user = User.objects.get(id=self.request.session.get('user_id'))
            if prof is not None and module is not None:
                obj = Score.objects.filter(user = user,professor = prof, module = module).first()
                if obj is not None:
                    obj.delete()
                serializer.save(professor = prof, module = module, user = user)
        except:
                return Response({"message":"No such professor or module!"},status=HTTP_400_BAD_REQUEST)


