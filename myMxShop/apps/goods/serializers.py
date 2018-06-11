__author__ = "zhaichuang"

from rest_framework import serializers
from goods.models import Goods,GoodsCategory,Banner
#drf 的序列化 json化model对象
# class GoodsSerializer(serializers.Serializer):
#     序列化字段
#     name = serializers.CharField(required=True,max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         '''
#         create and return
#         :param validated_data:
#         :return:
#         '''
#         return Goods.objects.create(**validated_data)

'''serializer的modelSerializer'''
#将子类实例化出来:

class CategorySerializer3(serializers.ModelSerializer):
    '''
    商品三级分类
    '''
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    '''
    商品二级分类
    '''
    sub_cat=CategorySerializer3(many=True) #覆盖子类别的字段显示子类的具体信息,many必须加,否则报错,因为子类也有多个
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    '''
    商品一级分类
    '''
    sub_cat=CategorySerializer2(many=True) #覆盖子类别的字段显示子类的具体信息否则报错,因为子类也有多个
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsSerializer(serializers.ModelSerializer):
      category = CategorySerializer()
      class Meta:
          model = Goods
          #序列化指定字段
          #fields = ("name","click_num",'market_price','add_time')
          #序列化所有的字段
          fields = '__all__'


#首页轮播图
class BannerSerializer(serializers.ModelSerializer):
    '''
    轮播图
    '''
    class Meta:
        model = Banner

