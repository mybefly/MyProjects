__author__ = "zhaichuang"
import paramiko
from GjWshile import readHarToFile
class connHost():
    '''
      链接远端服务器,然后上传脚本并执行命令
    将结果发送回来
    '''
    def __init__(self,host,port,username,password,projectPath):
        '''
        :param host: 远端主机
        :param port: 链接端口
        :param username: 登陆用户名
        :param password: 登陆密码
        :param projectPath: 项目地址
        :return:
        '''
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.projectPath=projectPath
        self.__mkdirForProject()
    def __mkdirForProject(self):
            '''
            :return:
            '''
            if   self.conn_exec("ls %s"%(self.projectPath))[1]:
                 self.conn_exec("mkdir %s"%(self.projectPath))

            if self.conn_exec("ls %s/shfiles"%(self.projectPath))[1]:
                 print(self.conn_exec("mkdir %s/shfiles"%(self.projectPath)))

            if self.conn_exec("ls %s/logfiles"%(self.projectPath))[1]:
                 self.conn_exec("mkdir %s/logfiles"%(self.projectPath))

            if self.conn_exec("ls %s/result"%(self.projectPath))[1]:
                 self.conn_exec("mkdir %s/result"%(self.projectPath))


    def conn_exec(self,cmd):
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.host,username=self.username,password=self.password)
            stdin,stdout,stderr = ssh.exec_command(cmd)
            return stdout.readlines(),stderr.readlines()
        except Exception as e:
            print(e)
    def put_file(self,localPath,remotepath):
        try:
            t=paramiko.Transport((self.host,self.port))
            t.connect(username=self.username,password=self.password)
            sftp=paramiko.SFTPClient.from_transport(t)
            sftp.put(localPath,remotepath)
            t.close()
        except Exception as e:
            print(e)
    def get_file(self,remotepath,localhost):
        try:
            t=paramiko.Transport((self.host,self.port))
            t.connect(username=self.username,password=self.password)
            sftp=paramiko.SFTPClient.from_transport(t)
            sftp.put(remotepath,localhost)
            t.close()
        except Exception as e:
            print(e)
if __name__=="__main__":
    remote_host=connHost("172.16.13.158",22,"root","whistle@ruijie.com.cn",projectPath="/home/GJ_MS")
