#!/usr/bin/env python3

import time
import sys
import socket
import threading
import re
import pymysql
from danmu import *


def  main():
  i = 1
  count_Heart = 0
  conut = 0
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)
  rid = input('please enter a room id:')
  GetDm = GetDanmu(rid)


  GetDm.connect(s) 
  GetDm.login(s)
  if GetDm.Is_alive():
    while i:
      byt = s.recv(1024)
      DM = GetDm.clean(byt) 
      if count_Heart > 5:
        if GetDm.Is_alive():
           count_Heart = 0
           GetDm.Heart(s)
        else:
           break
      if DM == None:
        count_Heart += 1
        continue
      print(DM)
      print('\n')
  else:
    print('the live_room has closed')
main()
