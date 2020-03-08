from django.shortcuts import render

# Create your views here.

import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

def __get_response_json_dict(data, err_code=0, message="Success"):
    ret = {
    'err_code': err_code,
    'message': message,
    'data': data
    }
    return ret

def user_register(request):
    received_data = json.loads(request.body.decode('utf-8'))

    username = received_data["username"]
    password = received_data["password"]

    user = User(username=username)
    user.set_password(password)

    user.save()

    return JsonResponse(__get_response_json_dict(data={}))

def user_login(request):
    received_data = json.loads(request.body.decode('utf-8'))

    username = received_data["username"]
    password = received_data["password"]

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse(__get_response_json_dict(data={}))
    else:
        return JsonResponse(__get_response_json_dict(data={}, err_code=-1, message="Invalid username or password"))

@login_required
def user_detail(request):

    response_data = {"username": request.user.username}

    return JsonResponse(__get_response_json_dict(data=response_data))


def user_logout(request):
    logout(request)
    return JsonResponse(__get_response_json_dict(data={}))