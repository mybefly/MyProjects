__author__ = "zhaichuang"
from django.views.generic import View #导入通用试图类
from .models import Goods

class GoodsListView(View): #通用视图
    def get(self,request):
    #通过Django的View类实现商品列表页面
        json_list = []
        goods = Goods.objects.all()
        print(goods)
        ''' 最原始的方法把model的内容转换为json
        for good in goods:
            json_dict = {}
            #获取商品的每个字段，键值对形式
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            json_list.append(json_dict)
        '''

        '''第二种方式 使用 model_to_json 将model字段转换为字典
           但是imagefield转成json报错,用第三种方式 Django自带的serializable

        from django.forms.models import model_to_dict
        for good in goods:
            json_dict = model_to_dict(good)
            json_list.append(json_dict)

        from django.http import HttpResponse
        import json
        return HttpResponse(json.dumps(json_list),content_type='application/json')
        '''
        '''
        第三种 使用Django.core 自带的serializable 序列化
        '''
        import json
        from django.core import serializers
        from django.http import JsonResponse

        json_data = serializers.serialize("json",goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data,safe=False)
