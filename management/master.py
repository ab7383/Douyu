#!/usr/bin/env python3
import queue
from multiprocessing.managers import BaseManager

class Job(object):
  
  def __init__(self):
    self.room_list = []
    with open("../room_list","r") as f:
      Anchos = f.readlines()
      for line in Anchos:
        Ancho = line.split()
        self.room_list.append(Ancho)
  
  def get_room(self):
    return self.room_list


class master(object):
  
  def __init__(self):
    self.room = []
    self.task_queue = queue.Queue()
    self.result_queue = queue.Queue()

 # def get_room(self):
 #   with open(~/Douyu/room_list) as f:
 #     Anchos = f.readlines()
 #     for line in Anchos:
 #       Ancho = line.split()
 #       self.room.append(Ancho)

  def send_job(self):
    BaseManager.register('get_task_queue',callable = lambda:self.task_queue)
    BaseManager.register('get_result_queue',callable = lambda:self.result_queue)
    
    manager = BaseManager(address=('',8888),authkey=b'jobs')
    manager.start()
    
    task_jobs = manager.get_task_queue()
    result_jobs = manager.get_result_queue()

    first_pos = 0
    group_size = 4
    second_pos = first_pos + group_size
    K = Job()
    job = K.get_room()
    
   # while len(job) >= second_pos :
    limit = 8
    while limit >= second_pos:
      n = job[first_pos : second_pos]  
      print("正在分配直播间")
      print(str(first_pos) + "到" + str(second_pos) + '\n')
      first_pos += group_size
      second_pos = first_pos + group_size

      task_jobs.put(n)
    
    print("等待抓取..."+'\n')
    one_pos = 0
    length = task_jobs.qsize()
    while length > one_pos:
      r = result_jobs.get()
      print("一个直播间抓取完成")
      one_pos += 1
    
    manager.shutdown()


if __name__ == '__main__':
  master =master()
  master.send_job()
