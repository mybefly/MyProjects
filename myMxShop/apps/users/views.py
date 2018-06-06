from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import UserProfile
from rest_framework.response import Response
# Create your views here.

class UserList(APIView):
    '''
    用户列表
    '''
    def get(self,request):
        users = UserProfile.objects.all()
        users_serializer = UserSerializer(users,many=True)
        return Response(users_serializer.data)

