"""myMxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
#不适用默认admin,使用xadmin
from django.urls import path,include
import xadmin
from django.views.static import serve
#导入drf的文档管理urls
from rest_framework.documentation import include_docs_urls
from myMxShop.settings import MEDIA_ROOT
#from goods.view_base import GoodsListView
from goods.views import GoosListViewSet
from users.views import UserList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()    #实例化 DefaultRouter
router.register("goods",GoosListViewSet)

urlpatterns = [
    #xadmin 配置
    path('xadmin/', xadmin.site.urls),
    path('ueditor/',include('DjangoUeditor.urls')),
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    #drf文档路由,title为标题
    path('docs/',include_docs_urls(title='练习生鲜系统')),
    #配置drf的urls
    path('api-auth/',include_docs_urls('rest_framework.urls')),

    #个人接口配置
    path('^',include('router.urls')),
    #path('goods/',GoosListView.as_view(),name='goods-list'),
    path('users/',UserList.as_view(),name='users-list')


]
