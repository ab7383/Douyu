#/usr/bin/env python3

from danmu import *
import sys
import multiprocessing

rid = ['156277','78561']
limit_time = input ('how long would you want to Get: ')

Get1 = GetDanmu(rid[0],limit_time)
Get2 = GetDanmu(rid[1],limit_time)
Get = [Get1,Get2]
def GetDM(Get):
  Get.run()
#多进程写法
#p_1 = multiprocessing.Process(target = GetDM, args=(Get1,))
#p_2 = multiprocessing.Process(target = GetDM, args=(Get2,))
#p_1.start()
#p_2.start()
#p_1.join()
#p_2.join()
#进程池写法
pool = multiprocessing.Pool(processes = 2)
for i in range(len(rid)):
  pool.apply_async(GetDM,(Get[i],))
pool.close()
pool.join()

