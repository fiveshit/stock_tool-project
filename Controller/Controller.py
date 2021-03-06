from Controller.error_msg import *
from View.View import Stock_View
from Model.Model import Stock_Mode
from Model.tw_stock_setting import Setting
from Model.tw_stock import tw_stock_analytics
from Model.tw_stock_load import load_stock_tables
from Model.tw_stock import BEST_BUY,BEST_SELL

from Model.tw_stock_tdcc import *
import twstock

from threading import Thread
from threading import Event
import threading
#---------------------------------------#
#Name : Stock_Controller
#Description : View want to call Model functions from controller interface
#Input : -
#Output : -
#Return : -
#---------------------------------------#
class Stock_Controller:
    def __init__(self):
        self.model = Stock_Mode()
        self.view = Stock_View()
        self.setting = Setting()
        self.stock = tw_stock_analytics()
        self.view.tw_stock_view_set_to_controller(self)
        self.view.tw_stock_view_init_ui()

        # flags
        self.flag_items = list(Flags)
        self.flag_items[Flags.REALTIME_LOOP.value] = False
        self.flag_items[Flags.INIT_FIG.value] = False
        self.flag_items[Flags.TEXT_STUCK.value] = False
        self.flag_items[Flags.REALTIME_START.value] = True

        # realtime thread
        self.event = Event()
        self.lock = threading.Lock()
        realtime = Thread(target = self.view.tw_stock_view_realtime,args=(self.event,self.lock,self.flag_items,))
        realtime.setDaemon(True)
        realtime.start()
    def run(self):
        self.view.window.protocol("WM_DELETE_WINDOW",self.tw_stock_controller_close)
        self.view.window.mainloop()
    def tw_stock_controller_close(self):
        if self.view.tw_stock_view_on_close():
            if self.flag_items[Flags.REALTIME_START.value] == True:
                self.flag_items[Flags.REALTIME_LOOP.value] = False
            if self.flag_items[Flags.REALTIME_START.value] == True:
                self.flag_items[Flags.REALTIME_LOOP.value] = False
            self.event.clear()
            self.view.window.destroy()
    def tw_stock_controller_realtime_run(self,realtime_id,realtime_text):
        self.realtime_id = realtime_id
        if self.flag_items[Flags.REALTIME_LOOP.value] == True:
            self.flag_items[Flags.REALTIME_LOOP.value] = False
            realtime_text.set("real time start")
        elif self.flag_items[Flags.REALTIME_LOOP.value] == False:
            self.flag_items[Flags.REALTIME_LOOP.value] = True   
            self.flag_items[Flags.INIT_FIG.value] = False
            realtime_text.set("running")
        if not self.event.is_set():
            self.event.set()
    def tw_stock_controller_stop(self,event):
        if self.flag_items[Flags.TEXT_STUCK.value] == False:
            self.flag_items[Flags.TEXT_STUCK.value] = True
    def tw_stock_controller_start(self,event):
        if self.flag_items[Flags.TEXT_STUCK.value] == True:
            self.flag_items[Flags.TEXT_STUCK.value] = False
#----- Setting function enum-------#
#    LOAD_SECTION = 0
#    LOAD_ALL_ITEMS = 1
#    CONFIG_READ = 2
#    CONFIG_WRITE = 3
#    CONFIG_SET = 4
#    CONFIG_GET = 5
#    CONFIG_DEL = 6
#------------------------------#
    def tw_stock_controller_setting(self,item,*args):
        if item == Setting_item.LOAD_SECTION:
            print("do load section")
        elif item == Setting_item.LOAD_ALL_ITEMS:
            print("do LOAD_ALL_ITEMS")
            return self.setting.Setting_load_all_items(self.setting.section_name)  
        elif item == Setting_item.CONFIG_READ:
            print("do config read")
        elif item == Setting_item.CONFIG_WRITE:
            print("do config write")
        elif item == Setting_item.CONFIG_SET:
            self.setting.Setting_config_set(self.setting.section_name,args[0],args[1])
        elif item == Setting_item.CONFIG_GET:
            print("do config get")
        elif item == Setting_item.CONFIG_DEL:
            self.setting.Setting_config_del(self.setting.section_name,args[0])
            print("do config delete")
    #---------load functions -----------#
    def tw_stock_load_data(self,path):
        return load_stock_tables(path)
        # -------TDCC functions-----------#
        #   TDCC_LOAD_DATE = 0
        #   TDCC_LOAD_DATA = 1
        #   TPEX_LOAD_INFO = 2
        #   TWSE_LOAD_INFO = 3
        #-------------------------------#
    def tw_stock_controller_tdcc(self,item,*args,period='D'):
        if item == TDCC_item.TDCC_LOAD_DATE:
            print("do TDCCC load date")
        elif item == TDCC_item.TDCC_LOAD_DATA:
            TDCC_load_stock_data(args[0],args[1],args[2])
        elif item == TDCC_item.TPEX_LOAD_INFO:
            return TPEx_load_stock_info(args[0],period)
        elif item == TDCC_item.TWSE_LOAD_INFO:
            return TWSE_load_stock_info(args[0])
    def tw_stock_controller_param_TPEx(self):
        return TPEx
        #----- stock  function enum-------#
        #   STOCK_LOAD_NUMBER = 0
        #   STOCK_LOAD_SHOW_DATA = 1
        #   STOCK_LOAD_HISTORY_DATA = 2
        #   STOCK_LOAD_HISTORY_TRANSACTION = 3
        #   STOCK_LOAD_REALTIME = 4
        #   STOCK_LOAD_BEST_FOURPOINT = 5
        #------------------------------#
    def tw_stock_controller_stock(self,item,*args):
        if item == Stock_item.STOCK_LOAD_NUMBER:
            return self.stock.load_stock_number(args[0])
            print("do load number")
        elif item == Stock_item.STOCK_LOAD_SHOW_DATA:
            print("do load show data")
        elif item == Stock_item.STOCK_LOAD_HISTORY_DATA:
            self.stock.load_stock_history_data(args[0],args[1],args[2])
            print("do load history data")
        elif item == Stock_item.STOCK_LOAD_HISTORY_TRANSACTION:
            self.stock.load_stock_history_transaction(args[0])
            print("do load history transaction")
        elif item == Stock_item.STOCK_LOAD_REALTIME:
            return self.stock.load_stock_realtime(self.realtime_id,args[0])
            print("do load realtime")
        elif item == Stock_item.STOCK_LOAD_BEST_FOURPOINT:
            stock_id = args[0]
            stock_id_get = args[1]
            if stock_id_get == "":
                merge_best_but_sell = self.stock.load_stock_BestFourPoint(stock_id)
                return
            stock_id = twstock.Stock(stock_id_get)
            merge_best_but_sell = self.stock.load_stock_BestFourPoint(stock_id)
            return merge_best_but_sell
    def tw_stock_controller_BEST_BUY(self):
        return BEST_BUY
    def tw_stock_controller_BEST_SELL(self):
        return BEST_SELL
       #-------- Model functions---------#
    def tw_stock_controller_model(self,tmp):
        return self.model.stock_mode_pd_to_datetime(tmp)

        
        











