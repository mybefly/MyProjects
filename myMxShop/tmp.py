__author__ = "zhaichuang"
import requests
import json
url = "https://apitest.dlut.edu.cn/api/v2/index.php/notification/sendNotificationFromDr?access_token=jLFjDPWD1iguijhFCTvPxi1B6z3vwm0l"
data = '''{
   "touser": "11017012|201723332",
   "msgtype": "news",
   "type": "5",
   "from": "11017012",
   "platforms":"whistle|weixin|qq",
   "news": {
       "articles":[
           {
               "title":"_)(:?><~!@#$%^&*{}|fjren发件人f发件人发47586957",
               "description": "+_)(:?><~                                                                                                                    fjren发件人f发件人发47586957!@#$%^&*{}|卡通漫画通漫通漫通漫通漫通漫通漫通漫通漫通卡通漫画通漫通漫通漫通漫通漫通漫通漫通漫通漫通漫通漫通漫通漫通漫通漫re图片漫通漫通漫通漫通漫通漫通漫                                                                                      r                   e图片",
               "url":"",
               "schema":"",
               "picurl":""
           }
        ]
   }
}'''
data = json.loads(data)
for i in range(17):
    rps = requests.post(url,json=data,verify=False)
    print(rps.json())