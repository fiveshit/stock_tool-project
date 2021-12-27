# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from error_msg import sys_debug_info
from error_msg import Flags


class analysis():
  def __init__(self):
      self.x_num = 7
      self.y_num = 8 #8-15
      self.figID = 1
  def create_transaction_barh_graph(self,x,y):
      plt.barh(y,x,1)
      plt.yticks(y)
      plt.title('transaction')
      plt.show()
  def create_ani_bar_graph(self,stock_id,x_price,y_price,x,y,flag_items=None):
      try:
          if flag_items[Flags.INIT_FIG.value] == False:
              flag_items[Flags.INIT_FIG.value] = True
              if plt.fignum_exists(self.figID):
                  print("TEST")
                  plt.close(self.fig)
              self.fig = plt.figure(self.figID,figsize=(8,6))
              #plt.ion()
          #plt.clf()
          x.reverse()
          x_price.reverse()
          buy_price = []
          sell_price = []
          # 取小數點後一位
          for i,j in zip(x_price,y_price):
              buy_price.append(i[0:-3])
              sell_price.append(j[0:-3])
          totle_price = buy_price + sell_price
          x = list(map(int,x))
          y = list(map(int,y))
          for i in y:
              x.append(i)
          bars = plt.bar(totle_price,x)
          self.create_Labels(bars)
          plt.xlabel("buy                  sell")
          plt.title(stock_id)
          plt.draw()
          plt.pause(0.001)
          self.fig.clear()
      except Exception as e:
          sys_debug_info(e)
          pass
      
  def create_line_graph(self,stock,data):
      analysis_stock_pd = pd.DataFrame(data)
      analysis_stock_pd = analysis_stock_pd.set_index('date')
      analysis_fig = plt.figure(figsize=(10,6))
      plt.plot(analysis_stock_pd.close,'-',label="closed_price")
      plt.title(stock.sid,loc='right')
      plt.xlabel('date')
      plt.ylabel('closed_price')
      plt.grid(True, axis='y')
      plt.legend()
      plt.show()
  def create_sum_line_graph(self,stock,data):
      analysis_stock_pd = pd.DataFrame(data)
      y = ['50,001','100,001','200,001','400,001','600,001','800,001','1,000,001 up']
      plt.plot(y,data[0][8:],color='green',linestyle='-',label='one_week_ago')
      plt.plot(y,data[1][8:],color='blue',linestyle='-',label='two_week_ago')
      plt.plot(y,data[2][8:],color='red',linestyle='-',label='three_week_ago')
      plt.plot(y,data[3][8:],color='yellow',linestyle='-',label='four_week_ago')
      plt.plot(y,data[4][8:],color='black',linestyle='-',label='five_week_ago')
      plt.title(str(stock))
      plt.legend(loc='upper right')
      plt.show()
  def create_Labels(self,data):
      for item in data:
          height= item.get_height()
          plt.text(item.get_x()+item.get_width()/2.,\
                   height*1.05,\
                   '%d' % int(height),\
                   ha='center',\
                   va= 'bottom')
  def create_bar_graph(self,stock,y):
      x = np.arange(self.x_num)
      colors = ['green','blue','red','yellow','white']
      labels = ['new1','new2','new3','new4','new5']
      width=0.1
      A=plt.bar(x,y[0][self.y_num:],width,color='green', label='one_week_ago')
      B=plt.bar(x+width,y[1][self.y_num:],width,color='blue', label='two_week_ago')
      C=plt.bar(x+(width*2),y[2][self.y_num:],width,color='red',label='three_week_ago')
      D=plt.bar(x+(width*3),y[3][self.y_num:],width,color='yellow',label='four_week_ago')
      E=plt.bar(x+(width*4),y[4][self.y_num:],width,color='black',label='five_week_ago')
      if self.y_num==15:
          z=['1-999','1,000','5,001','10,001','15,001','20,001','30,001','40,001',\
            '50,001','100,001','200,001','400,001','600,001','800,001','1,000,001 up']
      else:
          z = ['50,001','100,001','200,001','400,001','600,001','800,001','1,000,001 up']
      plt.xticks(x,z)
      plt.title(str(stock))
      self.create_Labels(A)
      self.create_Labels(B)
      self.create_Labels(C)
      self.create_Labels(D)
      self.create_Labels(E)
      plt.legend(bbox_to_anchor=(1,1), loc='upper left')

      
      plt.show()
