#/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup


class Get_room(object):

  def __init__(self):
    pass 
  def Parser(self,url):
    soup = BeautifulSoup(urlopen(url),'html.parser')
    return soup
 
  def Get_Ancho(self):
    page = 1
    Ancho_List = []

    print("正在抓取房间"+"\n")
    while page <= 50:
      url = "https://www.douyu.com/directory/all?page={page}&isAjax=1".format(page = page)
      soup = self.Parser(url)
      page +=1
      Anchos = soup.findAll("li")

      for Ancho in Anchos:
        Ancho_name = Ancho.find("span",{"class","dy-name ellipsis fl"}).get_text()
        Ancho_rid = Ancho.attrs["data-rid"]
        Ancho = (Ancho_name,Ancho_rid)
        Ancho_List.append(Ancho)
   
    with open('room_list','w') as f:
      print("正在写入房间"+"\n")
      for Anchos in Ancho_List:
        f.write(str(Anchos[1])+" "+str(Anchos[0])+'\n')
    print("完成！")


room = Get_room()
room.Get_Ancho()
