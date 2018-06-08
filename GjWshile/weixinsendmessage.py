__author__ = "zhaichuang"
import itchat

itchat.auto_login(hotReload=True)  #热登录


user = itchat.search_friends(nickName="")
username=user[0]["UserName"]

# itchat.send("哈哈哈哈哈")

#print(itchat.search_friends(nickName="文件传输助手"))
# rooms = itchat.get_chatrooms()
# for r in rooms:
#     print(r["NickName"])

#获取好友列表

# frendsList = itchat.get_friends()
# for f in frendsList:
#     # print("[%s] : %s"%(f["NickName"],f["UserName"]))
#     if 'helper' in f["UserName"]:
#         print(f['UserName'])

