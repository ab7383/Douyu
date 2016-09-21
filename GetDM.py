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
  count = 0
  limit = 5
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  rid = input('please enter a room id:')
  GetDm = GetDanmu(rid)


  GetDm.connect(s) 
  GetDm.login(s)
  while i == 1:
    byt = s.recv(1024)
    DM = GetDm.clean(byt) 
    if count > limit:
      count = 0
      GetDm.Heart(s)
    if (DM==None):
      count = count + 1
      continue
    print(DM)
    print('\n')

main()
