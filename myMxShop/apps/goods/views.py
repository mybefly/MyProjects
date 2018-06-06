from django.shortcuts import render
from rest_framework.views import APIView  #使用resetFramwork的APIView实现商品列表
from goods.serializers import GoodsSerializer  #导入定义的 serializers
from .models import Goods
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination #分页配置
from rest_framework import viewsets

# Create your views here.


'''继承的 APIView'''
# class GoosListView(APIView):
#     '''
#     商品列表
#     '''
#     def get(self,request,format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods,many=True)
#         return Response(goods_serializer.data)
#
#     def post(self,request,format=None):
#         serializer = GoodsSerializer(data=request.data)#获取前端发送过来的数据
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

'''继承mixin generics
   mixins.ListModelMixin
   mixins.CreateModelMixin
   mixins.RetrieveModelMixin
   mixins.UpdateModelMixin
   generics.GenericAPIView 必须加这个
'''

# class GoosListView(mixins.ListModelMixin,generics.GenericAPIView):
#     '''
#     商品列表
#     '''
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self,request, *args, **kwargs):
#          return self.list(request,*args,**kwargs)
'''
    直接继承gemerics.ListView 可直接省略 get方法
'''
#使用分页
class GoodsPagination(PageNumberPagination):
    page_size = 10 #默认每页显示几条数据
    page_size_query_param = 'page_size'  #配置每页显示多少条数据
    page_size_query_description = "每页显示多少条数据 使用方式 page_size= 数值"
    page_query_param = 'p' #请求时用的参数,页码 第几页
    page_query_description = "请求的页码数 比如 第 1页 第2页... p=数值"
    max_page_size = 100
#
# class GoosListView(generics.ListAPIView):
#     '''
#     商品列表
#     '''
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     '''
#         进行分页:第一种方式 settings.py中设置 REST_FRAMEWORK={配置}
#         第二种方式,继承 rest_framework.pagination.PageNumberPagination 在类中配置 请求需要的参数,默认显示数据条数等信息
#         然后再需要的类中使用 pagination_class = GoodsPagination
#
#     '''
#     pagination_class = GoodsPagination

#使用viewsets.GenericViewSet + routers方法
class GoosListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    商品列表
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    '''
        进行分页:第一种方式 settings.py中设置 REST_FRAMEWORK={配置}
        第二种方式,继承 rest_framework.pagination.PageNumberPagination 在类中配置 请求需要的参数,默认显示数据条数等信息
        然后再需要的类中使用 pagination_class = GoodsPagination

    '''
    pagination_class = GoodsPagination


