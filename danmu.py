#!/usr/bin/env python3
import time
import sys
import socket
import re
import threading
from urllib.request import urlopen


class GetDanmu(object):

  def __init__(self,name,room ,Time_Limit = 7200):
    self.name = name
    self.room = room
    self.Time_Limit =float(Time_Limit)
    self.gif_list = {'191':'100鱼丸','192':'一个赞','193':'2毛钱','194':'6块钱','195':'100块钱','196':'500块钱'}
    self.logout = "type@=logout/".encode('utf-8')
    self.DMserverStr = "type@=joingroup/rid@={self.room}/gid@=-9999/\0".format(self = self).encode('utf-8')
    self.LoginStr = "type@=loginreq/roomid@={self.room}/\0".format(self = self).encode('utf-8')
    self.Html = "https://www.douyu.com/{self.room}".format(self = self)
    self.HB = "type@=keeplive/tick@=1439802131\0".encode('utf-8')
    self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

  def Getname(self):
    return self.name
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
  def login(self):
    print (self.LoginStr)
    self.s.send(self.Message(self.LoginStr))
    self.s.recv(512)
    self.s.send(self.Message(self.DMserverStr))
#登出弹幕服务器
  def Log_out(self):
    self.s.send(self.Message(self.logout))
#连接弹幕服务器端口   
  def connect(self):
    port = 8602
    self.s.connect(("openbarrage.douyutv.com",port))
#发送心跳
  def Heart(self):
    while 1:
      time.sleep(25)
      self.s.send(self.Message(self.HB))
# 计时器
  def tick(self):
    global Time_Last, Time_Begin
    Time_Last = time.time() - Time_Begin
#整理转化unicode数据
  def clean(self,byt):
    Time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #判断是礼物还是弹幕
    try: 
      type = re.search(b'type@=.*?\/',byt).group(0).decode()
      type = re.search('[^type@=]\D+[^\/]',type).group(0)
    except Exception as e:
      return None
    #如果是弹幕,标记1
    if type == 'chatmsg':
      try:
        txt = re.search(b'txt@=.*?\/',byt).group(0).decode()
        txt = re.search('[^txt@=]\D*\d*[^\/]',txt).group(0)
        DM = [Time,txt,1]
        return DM
      except Exception as e:
        return None
    #如果是礼物，标记2
    elif type == 'dgb':
      try:
        gif_id = re.search(b'gfid@=\d+?\/',byt).group(0).decode()
        gif_id = re.search('\d+',gif_id).group(0)
        gif = [Time,'主播收到了'+self.gif_list[gif_id],2]
        return gif
      except Exception as e:
        return None
    #如果是关播推送，标记0
    elif type == 'rss':
      close_msg = re.search(b'ss@=\d\/',byt).group(0).decode()
      close_msg = re.search('\d',close_msg).group(0)
      if close_msg == 0:
        msg = [Time,'主播关闭了他的直播间',0]
        return msg
    else:
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
    if DM[2] == 1:
      with open('./Danmu/{self.room}+{self.name}'.format(self = self),'a+') as f:
        f.write(str(DM[0]) +' : '+ str(DM[1]) + '\n') 
    if DM[2] == 2:
      with open('./Gift/{self.room}+{self.name}'.format(self = self),'a+') as f:
        f.write(str(DM[0]) +' : '+ str(DM[1]) + '\n')
#获取弹幕
  def Get(self):
    self.connect()
    self.login()
    global Time_Last,Time_Begin

    while self.Time_Limit >= Time_Last:
      try:
        byt = self.s.recv(1024)
      except Exception as e:
        if not self.Is_alive():
          break
        else:
          continue
      DM = self.clean(byt)
      if DM == None:
        continue
      elif DM[2] == 0:
        break
     # print(DM)
     # print('\n')
      self.WriteDM(DM)
      self.tick()

#运行程序
  def run(self):
    global Time_Begin,Time_Last
    Time_Begin = time.time()
    Time_Last = time.time() - Time_Begin

    #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    if self.Is_alive():
      t1 = threading.Thread(target = self.Heart, args=(),name = 'heart beat')
      t1.setDaemon(True)
      t1.start()
      self.Get()
      self.Log_out()
      print('抓取完成')
    else:
      print('直播间已经关闭')

