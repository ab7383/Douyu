#!/usr/bin/env python3

import time
import sys
import socket
import threading
import re
import pymysql
from danmu import *


def  main():
  global Time_Begain,Time_Last,Write
  Time_Begain = time.time()
  Time_Last = time.time() - Time_Begain

  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  rid = input('please enter a room id:')
  Time_Limit =int(input('How long would you want:'))
  GetDm = GetDanmu(rid)
  Write = Danmu_Write(rid)

  if GetDm.Is_alive():
    t2 = threading.Thread(target = GetDm.Heart, args=(s,))
    t2.setDaemon(True)
    t2.start()
    run(s,GetDm,Time_Limit)
    GetDm.Log_out(s)
    print('get danmu is complited')
  else:
    print('the live_room has closed')
  


def run(s,GetDm,Time_Limit):
    GetDm.connect(s)
    GetDm.login(s)
    global Time_Begain,Time_Last,Write

    while Time_Limit > Time_Last:
      try:
        byt = s.recv(1024)
      except Exception as e:
        if not GetDm.Is_alive():
          break
        else:
          continue
      DM = GetDm.clean(byt) 
      if DM == None:
        continue
      print(DM)
      Write.WriteDM(str(DM))
      print('\n')
      Time_Last = time.time() - Time_Begain
main()
