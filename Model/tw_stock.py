# -*- coding: UTF-8 -*-
import twstock
from twstock import BestFourPoint
import tkinter.ttk as ttk
import tkinter as tk
import time
import analysis
import pandas as pd
import threading


BEST_BUY = {'是否量大收紅':0,'是否量縮價不跌':0,'三日均價由下往上':0,'三日均價大於六日均價':0}
BEST_SELL = {'量大收黑':0,'量縮價跌':0,'三日均價由上往下':0,'三日均價小於六日均價':0}
#---------------------------------------#
#Name : tw_stock_analytics
#Description : twstock functions interface
#Input : flag item
#Output : -
#Return : -
#---------------------------------------#
class tw_stock_analytics():
    def __init__(self,flag_items=None):
        #BEST_BUT = dict.fromkeys(['是否量大收紅','是否量縮價不跌','三日均價由下往上','三日均價大於六日均價'],0)
        #BEST_SELL = dict.fromkeys(['量大收黑','量縮價跌','三日均價由上往下','三日均價小於六日均價'],0)
        self.tw_stock_analysis = analysis.analysis()
        self.flag_items = flag_items
        self.sell_value = 0
        self.buy_value = 0
        self.lock = threading.Lock()
    def load_stock_number(self,stock_id):
        try:
            return twstock.Stock(stock_id)
        except:
            print("stock = {} isn't exist".format(stock_id))
            return False
    def load_stock_show_data(self,stock_id):
        self.stock = twstock.Stock(stock_id)
        print(self.stock.sid)
        print(self.stock.price)
        print(self.stock.high)
    def load_stock_history_data(self,stock_id,years,monthes):
        self.stock = twstock.Stock(stock_id)
        time.sleep(3)
        data = self.stock.fetch_from(years,monthes)
        print(data)
        self.tw_stock_analysis.create_line_graph(self.stock,data)
    def load_stock_history_transaction(self,stock_id):
        self.stock = twstock.Stock(stock_id)
        time.sleep(3)
        self.tw_stock_analysis.create_transaction_barh_graph(self.stock.transaction,self.stock.date)
    def load_stock_realtime(self,stock_id,show_bar):
        stock = twstock.realtime.get(stock_id)
        if stock['success'] == True:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('max_colwidth',100)
            result = pd.DataFrame(stock).T.iloc[1:3]
            result.columns = ["股票代號","地區","股票名稱","公司全名","時間",\
                              "最心成交價","成交量","累積成交量",\
                              "委託買價","委託買量",\
                              "委託賣價","委託賣量",\
                              "	開盤價","最高價","最低價"]
            result = result.fillna(method='ffill').fillna(method='bfill')
            if show_bar == True:
                self.lock.acquire()
                self.tw_stock_analysis.create_ani_bar_graph(stock_id,result["委託買價"][1],result["委託賣價"][1],result["委託買量"][1],result["委託賣量"][1],flag_items=self.flag_items)
                self.lock.release()
            #### display all information ####
            #print(result.iloc[0])
            #print((result["委託賣價"][0])[0])
            #for x in range(0,5):
            #    self.sell_value = self.sell_value + float((result["委託賣量"][0])[x])
            #    self.buy_value  = self.buy_value + float((result["委託買量"][0])[x])
            #print(self.sell_value)
            #print(self.buy_value)
            ##################################
            return result
            try:
                if int(result["成交量"][1]) > 100:
                    print("upupup")
                else:
                    print("down down")
            except:
                print("pass")
            '''
            for x in range(0,5):
                print("{} \n".format(result.iat[0,x])) 
            for x in range(5,15):
                print("{} \n".format(result.iat[1,x]))

            '''
    def load_stock_BestFourPoint(self,stock_id):
        T_BEST_BUY  = dict.fromkeys(BEST_BUY,0)
        T_BEST_SELL = dict.fromkeys(BEST_SELL,0)
        bfp = BestFourPoint(stock_id)
        if bfp.best_buy_1() == True:
            T_BEST_BUY['是否量大收紅'] = 1
        if bfp.best_buy_2() == True:
            T_BEST_BUY['是否量縮價不跌'] = 1
        if bfp.best_buy_3() == True:
            T_BEST_BUY['三日均價由下往上'] = 1
        if bfp.best_buy_4() == True:
            T_BEST_BUY['三日均價大於六日均價'] = 1
        if bfp.best_sell_1() == True:
            T_BEST_SELL['量大收黑'] = 1
        if bfp.best_sell_2() == True:
            T_BEST_SELL['量縮價跌'] = 1
        if bfp.best_sell_3() == True:
            T_BEST_SELL['三日均價由上往下'] = 1
        if bfp.best_sell_4() == True:
            T_BEST_SELL['三日均價小於六日均價'] = 1
        return {**T_BEST_BUY,**T_BEST_SELL}
            
        
        
        
        
        
        




