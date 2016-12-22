#/usr/bin/env python3

from danmu import *
import sys
import multiprocessing


limit_time = 7200
def read_room(limit = 5):
  Ancho_list = []
  with open("./room_list","r") as f:
    Anchos = f.readlines()
    for line in Anchos:
      Ancho = line.split()
      Ancho_list.append(Ancho)
    return Ancho_list[:limit]

def Get(dy):
  dy.run()

Anchos = read_room()

#创建GetDanmu对象
dy = []
j = 0
for room in Anchos:
  room = GetDanmu(Anchos[j][1],Anchos[j][0],limit_time)
  #room = GetDanmu('yinzi',71415,limit_time)
  dy.append(room)
  j =j + 1
#进程池
pool = multiprocessing.Pool(processes = 10)
for i in range(len(Anchos)):
  pool.apply_async(Get,(dy[i],))
pool.close()
pool.join()





