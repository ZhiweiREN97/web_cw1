from rating import views
from django.urls import path, re_path

urlpatterns = [
    path('users/', views.UsersAPIView.as_view()),
    re_path('users/(?P<pk>\d+)/', views.UserAPIView.as_view(),name='user-detail'),

]
