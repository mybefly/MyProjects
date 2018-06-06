__author__ = "zhaichuang"

from rest_framework import serializers
from goods.models import Goods,GoodsCategory
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

class CategorySerializer(serializers.ModelSerializer):
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
