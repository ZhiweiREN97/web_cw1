from django.shortcuts import render
from rating.models import User, Score, Professor, Module
from rating.serializers import *
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rating.permissions import IsOwnerOrReadOnly
from decimal import Decimal, ROUND_HALF_UP
#Login
class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        if User.objects.get(username=username):
            user = User.objects.get(username=username)
        else:
            return Response('No such username or password!')
        if user.password == password:
            #user.id is a PK
            self.request.session['user_id'] = user.id
            print (self.request.session['user_id'])
            return Response('Login successful!', status=HTTP_200_OK)
        return Response('Password error', status=HTTP_400_BAD_REQUEST)

#Register
class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username__exact=username):
            return Response("Username exists",HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email):
            return Response("Email exists",HTTP_400_BAD_REQUEST)
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

#List all modules
class ModuleAPIView(ListAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    def get(self, request, *args, **kwargs):
        queryset = Module.objects.all()
        #Formatting the message to output prettytable
        message = "Code;Name;Year;Semester;Taught by\n"
        for i in queryset:
            count = 0
            message += i.module_id + ";" + i.module_name + ";" + str(i.year) + ";" + str(i.semester) + ";"
            for j in i.prof.all():
                if count==0:
                    message += j.p_id +", Professor " + j.firstname + j.lastname +"\n"
                    count +=1
                else:
                    pass
                    message += ";;;;" + j.p_id +", Professor " + j.firstname + j.lastname +"\n"
                    #message += ";;;;\n"                           
        return Response(message, status=HTTP_200_OK)

#Avg of one module one professor
class AvgAPIView(APIView):
    queryset = Score.objects.all()
    def post(self, request, format=None):
        data = self.request.data
        p_id = data.get('p_id')
        print ("pid",p_id)
        module_id = data.get('module_id')
        prof = Professor.objects.get(p_id=p_id)
        module = Module.objects.filter(module_id=module_id)
        m_sample = Module.objects.filter(module_id=module_id).first()
        module_name = m_sample.module_name
        avg = 0
        count = 0
        scoreset = Score.objects.all()#filter(professor = prof, module= module)
        for i in module:
            scoreset = Score.objects.filter(professor = prof, module=i)
            for j in scoreset:
                avg += j.score
                count += 1
        if count !=0:
            avg = Decimal(avg /count)
            avg = avg.quantize(Decimal('0'),rounding=ROUND_HALF_UP)
        message = "The rating of Professor %s (%s) in module %s (%s) is %.1f " %(prof.lastname, prof.p_id, module_name, m_sample.module_id,avg)
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
                avg_rating = Decimal(avg_rating / count)
                avg_rating = avg_rating.quantize(Decimal('0'),rounding= ROUND_HALF_UP)
            message = message + "The rating of professor %s (%s) is %.1f ;" %(i.lastname, i.p_id, avg_rating) 
        return Response(message,status=HTTP_200_OK)

#Rate the professors 
class RatingAPIView(APIView):
    queryset = Score.objects.all()
    serializer = ScoreSerializer
    def post(self, request, format=None):
        data = request.data
        try:
            prof_id = data.get("professor")
            m_id = data.get("module")
            semester = data.get("semester")
            year = data.get("year")
            rating = data.get("score")
            prof = Professor.objects.get(p_id=prof_id)
            module = Module.objects.get(module_id=m_id,prof = prof,semester=semester,year=year)
            user = User.objects.get(id=self.request.session.get('user_id'))
            if prof is not None and module is not None:
                obj = Score.objects.filter(user = user,professor = prof, module = module).first()
                if obj is not None:
                    obj.delete()
                Score.objects.create(professor = prof, module = module, user = user,score=rating)
                return Response("Rating successful!",status=HTTP_200_OK)
        except:
                return Response("No such professor or module!",status=HTTP_400_BAD_REQUEST)


