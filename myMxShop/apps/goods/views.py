from django.shortcuts import render
from rest_framework.views import APIView        #使用resetFramwork的APIView实现商品列表
from goods.serializers import GoodsSerializer,CategorySerializer,BannerSerializer   #导入定义的 serializers
from .filter import GoodsFilter
from .models import Goods,GoodsCategory,Banner  #导入app的项目模型类
from rest_framework.response import Response  #drf的response
from rest_framework import status  #drf 的状态
from rest_framework import mixins  #drf 的mixins 混合
from rest_framework import generics #drf 的通用类
from rest_framework.pagination import PageNumberPagination # drf的分页配置
from rest_framework import viewsets   #def的 viewsetß
from django_filters.rest_framework import DjangoFilterBackend   #Django_filters过滤依赖
from rest_framework import filters   #drf 的filters包

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
    商品列表，分页，搜索，过滤，排序
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
 # 设置filter的类为我们自定义的类
    #过滤
    filter_class = GoodsFilter
    #搜索
    search_fields = ('name', 'goods_brief', 'goods_desc')
    #排序
    ordering_fields = ('sold_num', 'shop_price')
    '''
        进行分页:第一种方式 settings.py中设置 REST_FRAMEWORK={配置}
        第二种方式,继承 rest_framework.pagination.PageNumberPagination 在类中配置 请求需要的参数,默认显示数据条数等信息
        然后再需要的类中使用 pagination_class = GoodsPagination

    '''
    pagination_class = GoodsPagination

#商品类别接口:
#注释的内容，在后面生成drf文档的时候会显示出来，所有要写清楚
#要想获取某一个商品的详情的时候，继承 mixins.RetrieveModelMixin  就可以了
class CategroyViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    list:
         商品类别
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    #序列化使用的类
    serializer_class = CategorySerializer

#轮播图
class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer