#!/usr/bin/env python3

import time
import sys
import socket
import threading
import re
import pymysql
from danmu import *


def  main():
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#  s.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)
  rid = input('please enter a room id:')
  GetDm = GetDanmu(rid)
  thread_list = []

  if GetDm.Is_alive():
    t2 = threading.Thread(target = GetDm.Heart, args=(s,))
    t1 = threading.Thread(target = run, args=(s,GetDm,))
    t1.start()
    t2.start()
  else:
    GetDm.Logout(s)
    print('the live_room has closed')


def run(s,GetDm):
    GetDm.connect(s)
    GetDm.login(s)

    while 1:
      byt = s.recv(1024)
      DM = GetDm.clean(byt) 
      if DM == None:
        continue
      print(DM)
      print('\n')
main()
