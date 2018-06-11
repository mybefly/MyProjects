__author__ = "zhaichuang"

import django_filters
from django_filters.rest_framework.filterset import FilterSet
from django.db.models import Q
from .models import Goods,GoodsCategory

class GoodsFilter(FilterSet):
    '''
    商品过滤
    '''
    pricemin = django_filters.NumberFilter(name='shop_price',lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name='shop_price',lookup_expr='lte')
    top_category = django_filters.NumberFilter(name='category',method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
         # 不管当前点击的是一级分类二级分类还是三级分类，都能找到。
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))


    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']
