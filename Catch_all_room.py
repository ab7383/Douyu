#/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup


class Get_room(object):

  def __init__(self):
    self.page = 1
    self.url_0 = "https://www.douyu.com/directory/all"
    self.url_1 = "https://www.douyu.com/directory/all?page={page}&isAjax=1".format(page = self.page)

  #def get_num(self,page):
   # return page.get_text()
  
  def Parser(self,url):
    soup = BeautifulSoup(urlopen(url),'html.parser')
    return soup
 
 # def Max_page(self):
   # soup_0 = self.Parser(self.url_0)
   # page1 = urlopen("https://www.douyu.com/directory/all")
   # soup_0 = BeautifulSoup(page1,"lxml")
   # page_list = soup_0.find(id="J-pager")
   # print(page_list)
   # max_page = max(map(self.get_num , page_list))
   # return int(max_page)


  def Get_Ancho(self):
    #max_page = self.Max_page
    Ancho_List = []

    print("正在抓取房间"+"\n")
    while self.page <= 50:
      soup = self.Parser(self.url_1)
      self.page +=1
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
