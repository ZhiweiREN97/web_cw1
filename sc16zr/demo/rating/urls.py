from rating.views import *
from django.urls import path, re_path,include
from rest_framework import routers


urlpatterns = [
    path('register/',UserRegisterAPIView.as_view()),
    path('login/',UserLoginAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    path('modules/',ModuleAPIView.as_view()),
    path('avg/',AvgAPIView.as_view()),
    path('allavg/',AllRatingAPIView.as_view()),
    path('rating/',RatingAPIView.as_view())
]
