#!/usr/bin/env python3
import time
import sys
import socket
import re
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

  def __init__(self,room):
    self.room = room
    self.logout = "type@=logout/".encode('utf-8')
    self.HB = "type@=keeplive/tick@=1439802131\0".encode('utf-8')
    self.DMserverStr = "type@=joingroup/rid@={self.room}/gid@=-9999/\0".format(self = self).encode('utf-8')
    self.LoginStr = "type@=loginreq/roomid@={self.room}/\0".format(self = self).encode('utf-8')
    self.Html = "https://www.douyu.com/{self.room}".format(self = self)


  def msgHead(self,msgstr):
    data_length = len(msgstr)+8
    code = 689
    msgHead =int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
    return msgHead

  def Message(self,msgS):
    msg = self.msgHead(msgS) + msgS
    return msg

  def login(self,s):
    print (self.LoginStr)
    s.send(self.Message(self.LoginStr))
    s.recv(512)
    s.send(self.Message(self.DMserverStr))

  def Heart(self,s):
    s.send(self.Message(self.HB))

  def Log_out(self,s):
    s.send(self.message(self.logout))
   
  def connect(self,s):
    port = 8601
    s.connect(("openbarrage.douyutv.com",port))

  def clean(self,byt):
    id = re.search(b'(uid@=)(.)*?\/',byt)
    nickname = re.search(b'(nn@=)(.)*?\/',byt)
    txt = re.search(b'(txt@=)(.)*?\/',byt)
    Time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if id==None or nickname==None or txt==None:
      return None
    else:
      try:
        id = id.group(0).decode()
        nickname = nickname.group(0).decode()
        txt = txt.group(0).decode()
        DM = (id,nickname,txt,Time)
        return DM
      except Exception as e:
        return None

  def Is_alive(self):
    try:
     status = re.search('''"show_status":.''' ,urlopen(self.Html).read().decode('utf-8')).group(0)
    except Exception as e:
      print("the room is not exist")
#    status = re.search('''"show_status":.''',H).group(0)
    status_value = int(re.search("[1-9]",status).group(0))
    if status_value == 1:
      return True
    else:
      return False

 
