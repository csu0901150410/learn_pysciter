#coding=utf-8

import socket;
import json;
import time;
import sys;

class socket_client:
    def __init__(self,ip='127.0.0.1',port=4066):
        self.sock = socket.socket()
        self.addr = (ip,port)
        self.start()
        
    def start(self):
        try:
            self.sock.connect(self.addr)
        except socket.error:
            print("网络端口连接失败，请检查端口")
            sys.exit(1)

    def _recv(self):
        total_data=bytes()
        the_strVale=[]
        end ='!script_message_end'     #接口tcp 结束消息为!script_message_end
        while True:
            data = self.sock.recv(1024)
            strValue = str(data,'gb2312')
            the_strVale.append(strValue)
            joinstr = ''.join(the_strVale)
            if end in joinstr:
                total_data = total_data + data
                break
            else:
                total_data = total_data + data
                
        totalstr = str(total_data,'gb2312')
        totalstr = totalstr[:totalstr.find(end)]
        return totalstr
          
    def send(self,msg:str):
        data = msg.encode("gb2312")
        self.sock.sendall(data)

    def stop(self):
        self.sock.close()

    def send_command(self,commandname,paramdict={}):
        dict = {}
        dict["name"] = commandname
        dict["arg"]  = paramdict
        
        jsonData = json.dumps(dict, ensure_ascii=False)
        # print('call api-'+jsonData)
        self.send(jsonData+'!script_message_end')
        retstr = self._recv()
        ret=json.loads(retstr)
        if not ret["success"]:
            print(ret)
        return ret