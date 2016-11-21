#!/usr/bin/env python3
import time
import sys
import socket
import re
import threading
from urllib.request import urlopen

class danmu (object):
  def __init__(self):
    self.__ID
    self.__txt
    self.__time 

  def getID(self):
    return self.ID
  def getTxt(self):
    return self.txt
  def getTime(self):
    return self.time

  def setID(self,ID):
    self.__ID = ID
  def setTxt(self,txt):
    self.__txt = txt
  def setTime(self,time):
    self.__time = time

class GetDanmu(object):

  def __init__(self,room ,Time_Limit):
    self.room = room
    self.Time_Limit =float(Time_Limit)
    self.logout = "type@=logout/".encode('utf-8')
    self.DMserverStr = "type@=joingroup/rid@={self.room}/gid@=-9999/\0".format(self = self).encode('utf-8')
    self.LoginStr = "type@=loginreq/roomid@={self.room}/\0".format(self = self).encode('utf-8')
    self.Html = "https://www.douyu.com/{self.room}".format(self = self)
    self.HB = "type@=keeplive/tick@=1439802131\0".encode('utf-8')
#包头处理
  def msgHead(self,msgstr):
    data_length = len(msgstr)+8
    code = 689
    msgHead =int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
    return msgHead
#发送信息格式统一处理
  def Message(self,msgS):
    msg = self.msgHead(msgS) + msgS
    return msg
#登录弹幕服务器
  def login(self,s):
    print (self.LoginStr)
    s.send(self.Message(self.LoginStr))
    s.recv(512)
    s.send(self.Message(self.DMserverStr))
#登出弹幕服务器
  def Log_out(self,s):
    s.send(self.Message(self.logout))
#连接弹幕服务器端口   
  def connect(self,s):
    port = 8602
    s.connect(("openbarrage.douyutv.com",port))
#发送心跳
  def Heart(self,s):
    while 1:
      time.sleep(25)
      s.send(self.Message(self.HB))
#整理转化unicode数据
  def clean(self,byt):
   # nickname = re.search(b'(nn@=)(.)*?\/',byt)
    txt = re.search(b'(txt@=)(.)*?\/',byt)
    Time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if txt==None:
      return None
    else:
      try:
       # nickname = nickname.group(0).decode()
        txt = txt.group(0).decode()
        txt = re.search('[^txt@=]\D*\d*[^\/]',txt).group(0)
        DM = (Time,txt)
        return DM
      except Exception as e:
        return None
#是否在直播
  def Is_alive(self):
    try:
     status = re.search('''"show_status":.''' ,urlopen(self.Html).read().decode('utf-8')).group(0)
    except Exception as e:
      print("the living-room is not exist")
    status_value = int(re.search("[1-9]",status).group(0))
    if status_value == 1:
      return True
    else:
      return False
#写入文件
  def WriteDM(self,DM):
    with open('./Danmu/{self.room}'.format(self = self),'a+') as f:
      f.write(DM+'\n') 
#获取弹幕
  def Get(self,s,Time_Limit):
    self.connect(s)
    self.login(s)
    global Time_Begain,Time_Last

    while self.Time_Limit > Time_Last:
      try:
        byt = s.recv(1024)
      except Exception as e:
        if not self.Is_alive():
          break
        else:
          continue
      DM = self.clean(byt)
      if DM == None:
        continue
     # print(DM)
      self.WriteDM(str(DM))
     # print('\n')
      Time_Last = time.time() - Time_Begain

#运行程序
  def run(self):
    global Time_Begain,Time_Last
    Time_Begain = time.time()
    Time_Last = time.time() - Time_Begain

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 # rid = input('please enter a room id:')
 # Time_Limit =int(input('How long would you want:'))

    if self.Is_alive():
      t1 = threading.Thread(target = self.Heart, args=(s,))
      t1.setDaemon(True)
      t1.start()
      self.Get(s,self.Time_Limit)
      self.Log_out(s)
      print('get danmu is complited')
    else:
      print('the live_room has closed')

