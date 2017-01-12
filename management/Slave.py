#/usr/bin/env python3


import queue
from multiprocessing.managers import BaseManager
import time
from run import *

class slave(object):
  def __init__(self):
    pass
  def start(self):
    BaseManager.register('get_task_queue')
    BaseManager.register('get_result_queue')
   

   # 连接master
    server = '222.18.159.11'
    print('Connect to server %s...' % server)
    manager = BaseManager(address=(server, 8888), authkey=b'jobs')
    manager.connect()

   # 使用上面注册的方法获取队列
    task_jobs = manager.get_task_queue()
    result_jobs = manager.get_result_queue()
    

    one_pos = 0
    length = task_jobs.qsize()
    while length > one_pos:
      room_list = []
      jobs = task_jobs.get()
      for job in jobs:
        room_list.append(job)
      run = Run(room_list)
      run.start()
      result_jobs.put(jobs)
      one_pos += 1

if __name__ == '__main__':
  slave = slave()
  slave.start()
