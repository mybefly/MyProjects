#coding:utf-8
__author__ = "zhaichuang"
import os,json,datetime,time,sys,jsonpath
import re

class readHar():
    def __init__(self,harfilePath,islocal=1,level=1,sqlmap='/Users/zhaichuang/Downloads/sqlmapTools'):
        '''
        :param level: 检测级别
        :param harfilePath:  har 源文件路径
        :param sqlmap:       sqlmap路径
        :return:
        '''
        self.level=level
        self.is_local=islocal
        self.sqlMapPath=sqlmap
        self.harpath = os.path.abspath(harfilePath)
        self.date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

        if os.path.isfile(self.harpath):
            self.basePath = os.path.abspath(self.harpath.split("/")[-2])
            self.platName=self.harpath.split("/")[-2]

            if os.path.isdir(self.basePath+"/%s_shfiles"%self.platName):
                self.shpath = self.basePath+"/%s_shfiles"%self.platName
            else:
                os.mkdir(self.basePath+"/%s_shfiles"%self.platName)
                self.shpath = self.basePath+"/%s_shfiles"%self.platName
            #-----logfile
            if os.path.isdir(self.basePath+"/%s_logfiles"%self.platName):
                self.logPath = self.basePath+"/%s_logfiles"%self.platName
            else:
                os.mkdir(self.basePath+"/%s_logfiles"%self.platName)
                self.logPath = self.basePath+"/%s_logfiles"%self.platName
            #-----result
            if os.path.isdir(self.basePath+"/%s_result"%self.platName):
                self.resPath = self.basePath+"/%s_result"%self.platName
            else:
                os.mkdir(self.basePath+"/%s_result"%self.platName)
                self.resPath = self.basePath+"/%s_result"%self.platName
        else:
            print("输入的har文件不存在")
    def readHarFile_Client(self,sqlmapth="",logpath="",level=""):
        '''
        读取har文件并生成sh文件
        :return:
        '''
        if self.is_local:
            pass
        else:
            self.sqlMapPath=sqlmapth
            self.logPath=logpath
            self.level=level
        getRequestList=[]
        postRequestList=[]
        if os.path.isfile(os.path.abspath(self.harpath)):
            with open(self.harpath,"r") as hf:
                harDic = json.loads(hf.read()) #将读取的文件转换成字典
                interface_info=harDic["log"]["entries"]
                # os.system("rm -rf %s/*"%self.shpath)
                for i in range(len(interface_info)):
                    reMethod = interface_info[i]["request"]["method"]
                    reUrl = interface_info[i]["request"]["url"]
                    if reMethod=="GET":
                       tmp1=reUrl.split("&")[:2] # 获取url
                       tmp2=reUrl.split("&")
                       tmp1="&".join(tmp1)+"="+str(+len(tmp2))
                       if tmp1 not in getRequestList:
                          getRequestList.append(tmp1)
                          with open(self.shpath+"/%d.sh"%i,"w") as shf:
                               shf.write("#!/bin/bash\n")
                               shf.write('python %s/sqlmap.py -u "%s" --level=%s --batch >>%s/%d.log'%(self.sqlMapPath,reUrl,self.level,self.logPath,i))
                               os.system("chmod 777 %s/%d.sh"%(self.shpath,i))
                    if reMethod=="POST":
                            oneRequestParams=[]
                            pars=[]
                            params = interface_info[i]["request"]["postData"]["params"]
                            for p in params:
                                oneRequestParams.append(p["name"])
                                pars.append("%s=%s"%(p["name"],p["value"]))
                            #print(oneRequestParams)index
                            if "index.php" in reUrl:
                                postTmp1=reUrl
                            postTmp2="&".join(oneRequestParams)
                            postTmp3=str(len(oneRequestParams))
                            postTmp ="%s&%s==%s"%(postTmp1,postTmp2,postTmp3)
                            if postTmp not in postRequestList:
                                postRequestList.append(postTmp)
                                with open(self.shpath+"/%d.sh"%i,"w") as shf2:
                                    par = "&".join(pars)
                                    shf2.write("#!/bin/bash\n")
                                    print('python %s/sqlmap.py -u "%s" --data "%s" --level=%s  --batch >>%s/%d.log'%(self.sqlMapPath,reUrl,par,self.level,self.logPath,i))
                                    shf2.write('python %s/sqlmap.py -u "%s" --data "%s" --level=%s --batch >>%s/%d.log'%(self.sqlMapPath,reUrl,par,self.level,self.logPath,i))
                                    os.system("chmod 777 %s/%d.sh"%(self.shpath,i))
                                    print(i)
                            # print(reUrl)
                            # print(par+"\n")
        else:
            print("文件不存在")

    def readHarFile_MS(self):
        #存放去重过滤掉资源请求后的API接口请求
        urldict = {}
        #如果存放sh的目录存在删除该目录下的文件
        if os.path.isdir(self.shpath):
            os.system("rm -rf %s/*"%self.shpath)

        if os.path.isfile(self.harpath):
            #=============读取har文件帅选请求=====================
            with open(self.harpath,"r") as hf:
                harDic = json.loads(hf.read())                      #将读取的文件转换为json格式
                requests = jsonpath.jsonpath(harDic,"$..request")   #查询出所有的
                #==================去重并过滤掉资源请求,将结果封装成字典返回=============================
                for request in requests:
                    method = request["method"]
                    url = request['url']
                    if 'api' in url and '?' not in url:
                        parms = request["postData"]["params"]  #获取所有的参数
                        paramlist =[]                          #参数+&列表 形式: 参数&参数
                        paramDataList =[]                      #参数+值+& 列表,形式: 参数=值&参数=值
                        for p in parms:
                            name = p['name']
                            value = p['value']
                            kv = name+'='+value
                            paramlist.append(name)
                            paramDataList.append(kv)
                        paramlist = "&".join(paramlist)
                        paramDataList="&".join(paramDataList)
                        urldict[paramlist]={'method':method,'url':url,'paramDataList':paramDataList}

                    elif 'api' in url and '?' in url:
                        #请求为post 但是形式为ip?params
                        urllist= url.split("?")
                        u = urllist[0]
                        p = urllist[1]
                        psplit = re.split(r'&|=',p)[::2]
                        paramList = "&".join(psplit)
                        urldict[paramList] ={'method':method,'url':u,'paramDataList':p}
                    else:
                        pass
                        #print("资源请求,非接口请求:%s"%url)
                #=============================================
                urldictlenth = len(urldict)
                print(urldictlenth)
                urlvs = list(urldict.values())
                for i in range(urldictlenth):
                    method = urlvs[i]['method']
                    url  = urlvs[i]['url']
                    paramDataList=urlvs[i]['paramDataList']
                    apiname=re.findall(r'm=(.*?)&a=(.*?)&',urlvs[i]['paramDataList'])[0] #获取接口名称
                    appnameM= apiname[0]
                    appnameA= apiname[1]
                    fileName = str(i+1)+"_"+appnameA.strip()
                    #print("m=%s,a=%s"%(apiname[0],apiname[1]))
                    #print("接口名称 : %s"%appnameA)
                    with open(self.shpath+"/%s.sh"%(fileName),"w") as shf:
                         shf.write("#!/bin/bash\n")
                         if method == "POST":
                            shf.write("python %s/sqlmap.py -u '%s' --data '%s' --level=%s --batch >>%s/%s.log"%(self.sqlMapPath,url,paramDataList,self.level,self.logPath,fileName))
                         else:
                            url = url+"?"
                            shf.write('python %s/sqlmap.py -u "%s" --batch >>%s/%s.log'%(self.sqlMapPath,url,self.logPath,fileName))
                    print(fileName)
                    os.system("chmod 777 %s/%s.sh"%(self.shpath,fileName))
        else:
            print("文件不存在")

    def readShTorun(self,):
        '''
        读取sh文件目录并运行
        :return:
        '''
        count=0
        if os.path.isdir(self.logPath):
            os.system("rm -rf %s/*"%self.logPath)
            time.sleep(1)
        if os.path.isdir(self.shpath):
            for f in os.listdir(self.shpath):
                os.system("rm -rf /Users/zhaichuang/.sqlmap/output/*")
                count=count+1
                print("运行次数:%s 文件:%s 正在运行.."%(count,f))
                os.system("sh %s/%s"%(self.shpath,f))
                print("sh %s/%s"%(self.shpath,f))
        else:
            print("sh目录不存在")
    def huigui(self,url=None,*shs):
        shslen=len(shs)
        count=0
        if shslen==0:
            sys.exit("无可执行sh文件")
        else:
            for sh in shs:
               os.system("rm -rf /Users/zhaichuang/.sqlmap/output/*")
               filename=self.shpath+"/"+str(sh)+".sh"
               count=count+1
               if url:
                   with open(filename,"r") as uf:
                       Lines=uf.readlines()
                       oneLine=Lines[1].replace("http://172.16.56.199",url)
                       oneLine2=oneLine.replace("school=weishao","school=yidongduan")
                       oneLine3=oneLine2.replace("verify=admin_auto_MS_weishao__web__5a0a9b4a95d1b__2fc13eeb5cf77825036868111fd68ba4__nAdYj3TwL4y56s7bRbwb5WC6Uas97lfNcX6e",
                                                 "verify=admin_yidongduan_MS_yidongduan__web__5a376e094ec96__3f025450907cbdb676e90c6040be39be__c91b717d-d35b-485b-ab8c-d3acfe05fde0")
                       print(oneLine3)
                       with open(filename,"w") as cf:
                            cf.write(Lines[0])
                            cf.write(oneLine3)

               print("运行次数:%s 文件:%s 正在运行.."%(count,str(sh)+".sh"))
               os.system("sh %s/%s"%(self.shpath,str(sh)+".sh"))
               print("sh %s/%s"%(self.shpath,str(sh)+".sh"))

    def countResult(self):
        '''
        读取结果
        :return:
        '''
        count=1
        tmp=[]
        if os.path.isdir(self.logPath):
            for f in os.listdir(self.logPath):
                if os.path.isfile("%s/%s"%(self.logPath,f)) and f.split(".")[1]=="log":
                    with open("%s/%s"%(self.logPath,f),"r") as lf,\
                         open("%s/%s_result_%s.txt"%(self.resPath,self.basePath.split("/")[-1],self.date),"a+") as rf:
                            for i in lf :
                               if "500" in i :
                                   with open("%s/%s.sh"%(self.shpath,f.split(".")[0]),"r") as shf:
                                       url=shf.readlines()[1].split("-u")[1].split("--level")[0].split("--data")
                                       url="".join(url)
                                       print(url+"\n")
                               if "Parameter: " in i:
                                   rf.write("\n")
                                   print("[序   号:] %s "%count)
                                   with open("%s/%s.sh"%(self.shpath,f.split(".")[0]),"r") as sf:
                                         urlr=sf.readlines()[1]
                                         urlall = urlr.split(" ")
                                         url = urlall[3].replace('"','')
                                         urldata = urlall[5].replace('"','')
                                         if "--data" in urlr:
                                            wurl="%s?%s".replace("\"","")%(url,urldata)
                                            interfaceName=wurl.split("a=")[1].split("&")[0]
                                         else:
                                             wurl=url
                                             interfaceName=url.split("a=")[1].split("&")[0]
                                         p = i.strip().split(":")[1]
                                         rf.write("[序   号:] %s \n"%count)
                                         print("[接口名称]: %s"%interfaceName)
                                         rf.write("[接口名称]: %s\n"%interfaceName)
                                   count+=1
                               if "Type:" in i:
                                     type=i.strip().split("Type:")[1].strip()
                               if "Title:" in i:
                                     title = i.strip().split("Title:")[1].strip()
                               if "Payload: " in i :
                                   data = i.strip().split("Payload:")[1].strip()
                                   if p not in tmp:
                                         tmp.append(p)
                                         print("[注入参数]:%s"%p)
                                         rf.write("[注入参数]:%s\n"%p)
                                   if type not in tmp:
                                        tmp.append(type)
                                        print("[注入类型]: %s"%type )
                                        rf.write("[注入类型]: %s\n"%type )
                                   if title not in tmp:
                                         tmp.append(title)
                                         print("[标   题]: %s"%title)
                                         rf.write("[标   题]: %s\n"%title)
                                   if data not in tmp:
                                       tmp.append(data)
                                       print("[注入数据]: %s "%data)
                                       rf.write("[注入数据]: %s \n"%data)
                                   if wurl not in tmp:
                                       tmp.append(wurl)
                                       print("[对应的log文件]: %s"%f)
                                       print("[完整URL]: %s"%wurl)
                                       rf.write("[对应的log文件]: %s\n"%f)
                                       rf.write("[完整URL]: %s\n"%wurl)
                                   rf.write("\n")

                tmp=[]

            # print(tmp)
        else:
            print("log目录不存在")
if __name__=="__main__":


    # dl_client= readHar("Client/1114_Gjclient.har",islocal=1)
    # dl_client.readHarFile_Client()
    # dl_client.readShTorun()
    #dl_client.countResult()

    gj_MS= readHar("MS/gaojiao.har",islocal=1)
    gj_MS.readHarFile_MS()
    # gj_MS.readShTorun()
    # gj_MS.countResult()
    #gj_MS.huigui("http://172.16.117.216:3000",*[0,1,101,103,104,15,22,32,35,39,4,44,54,56,60,65,67,69,7,71,75,76,81,87,91,93])
    #gj_MS.huigui("http://172.16.117.216:3000",*[0])
    #gj_MS.countResult()

