from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import UserProfile
from rest_framework.response import Response

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your views here.

User = get_user_model()

class UserList(APIView):
    '''
    用户列表
    '''
    def get(self,request):
        users = UserProfile.objects.all()
        users_serializer = UserSerializer(users,many=True)
        return Response(users_serializer.data)



class CustomeBackend(ModelBackend):
    '''
    自定义用户验证
    '''
    def authenticate(self,username=None,password=None,**kwargs):
        try:
            #用户名和手机登录
            user = User.objects.get(Q(username=username)|Q(mobile = username))
            if user.check_password(password):
                return user
        except Exception as  e:
            return None
