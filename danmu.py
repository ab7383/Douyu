#!/usr/bin/env python3
import time
import sys
import socket
import threading
import re
import pymysql

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
    self.HB = "type@=keeplive/tick@=1439802131\0"
    self.DMserverStr = "type@=joingroup/rid@={self.room}/gid@=-9999/\0".format(self = self)
    self.LoginStr = "type@=loginreq/roomid@={self.room}/\0".format(self = self)


  def msgHead(self,msgstr):
    data_length = len(msgstr)+8
    code = 689
    msgHead =int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
    return msgHead

  def Message(self,msgS):
    msgS = msgS.encode('utf-8')
    msg = self.msgHead(msgS) + msgS
    return msg

  def login(self,s):
    print (self.LoginStr)
    s.send(self.Message(self.LoginStr))
    s.recv(512)
    s.send(self.Message(self.DMserverStr))
    s.recv(512)
  
  def connect(self,s):
    port = 8601
    s.connect(("openbarrage.douyutv.com",port))

  def clean(self,byt):
    id = re.search(b'(uid@=)(.)*?\/',byt)
    nickname = re.search(b'(nn@=)(.)*?\/',byt)
    txt = re.search(b'(txt@=)(.)*?\/',byt)
    Time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
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

  def Heart(self,s):
    Hb = self.HB.encode('utf-8')
    heartbeat = self.msgHead(Hb)+Hb
    s.send(heartbeat)

