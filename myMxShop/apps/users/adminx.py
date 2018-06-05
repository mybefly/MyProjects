__author__ = "zhaichuang"

import xadmin
from xadmin import views   #这个views只是需要更改xadmin整体配置的时候才引入
from .models import VerifyCode

#添加主题功能
class BaseSetting(object):
    enable_themes = True    #开启主题功能
    use_bootswatch = True   #是否可以切换主题

#添加全局配置
class GlobleSetting(object):
    site_title = "My MxShop"  #导航左上角头部设置
    site_footer = "http://www.baidu.com"  #页脚设置
    menu_stye = 'accordion' #导航样式

#注册的model 在后台的显示配置
class VerifyCodeAdmin(object):
    list_display =["code","mobile","add_time"] #在后台显示的字段
#注册配置到xadmin 中的views中
xadmin.site.register(views.BaseAdminView,BaseSetting)
#注册全局配置到xadmin 中的views中
xadmin.site.register(views.CommAdminView,GlobleSetting)
#注册verifycode类
xadmin.site.register(VerifyCode,VerifyCodeAdmin)