from rating.views import *
from django.urls import path, re_path,include
from rest_framework import routers


urlpatterns = [
    path('users/', UsersAPIView.as_view()),
    re_path('users/(?P<pk>\d+)/', UserAPIView.as_view(),name='user-detail'),
    path('auth/', AuthView.as_view()),
    path('register/',UserRegisterAPIView.as_view()),
    path('login/',UserLoginAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    path('modules/',ModuleAPIView.as_view())
]
