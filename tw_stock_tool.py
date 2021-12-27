# -*- coding: UTF-8 -*-
import tkinter as tk
import time
import os
import pandas as pd
import twstock
from datetime import datetime
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from threading import Event
import threading
import matplotlib.pyplot as plt
from tkinter import messagebox

from error_msg import sys_debug_info
import tw_stock_tdcc
from tw_stock_tdcc import TDCC_load_stock_date,TDCC_load_stock_data,TPEx_load_stock_info, \
     TWSE_load_stock_info,TPEx
from tw_stock import BEST_BUY,BEST_SELL
import tw_stock
from tw_stock_load import load_stock_tables
from error_msg import Flags
import tw_stock_setting


class tw_stock_tool(tk.Tk):
    def __init__(self,window):
        self.app = window
        self.window = window.title('STOCK')
        window.geometry('820x650')
        self.tw_stock_tool_label(10,20)
        self.tw_stock_tool_entry(75,20)
        self.tw_stock_tool_button_stock_list("list",230,20)
        self.tw_stock_tool_check_button(75,50,75,70,175,50)
        self.tw_stock_tool_button(50,100)
        self.tw_stock_tool_tdcc_search(200,130)
        self.tw_stock_tool_realtime_button(50,130)
        self.tw_stock_tool_load_stock_table(50,160)
        self.tw_stock_tool_check_button_date(50,200,100,200,160,200)
        self.tw_stock_tool_bestfourpoint(200,100)
        self.tw_stock_tool_range_entry(120,162,190,162,165,162)
        self.tw_stock_tool_notebook(300,20)
        self.tw_stock_tool_get_buy_sell_info(50,230)
        self.tw_stock_tool_treeview_preview(0,350)
        self.tw_stock_tool_date_entry(120,260,50,260,165,230)
        self.tw_stock_tool_TPEx_TWSE_check_button(50,280)
        self.tw_stock_tool_rank_entry(240,260,180,260)
        
        
        #self.tw_stock_analytics.tw_stock_tool_notebook(self.window,0,200)
        self.flag_items = list(Flags)
        self.flag_items[Flags.REALTIME_LOOP.value] = False
        self.flag_items[Flags.INIT_FIG.value] = False
        self.flag_items[Flags.TEXT_STUCK.value] = False
        self.flag_items[Flags.REALTIME_START.value] = True
        #### tw_stock_analytics ###
        self.tw_stock_analytics = tw_stock.tw_stock_analytics(self.flag_items)
        ### tw_stock_setting ###
        self.tw_stock_setting = tw_stock_setting.Setting()
        self.event = Event()
        realtime = Thread(target = self.tw_stock_tool_realtime)
        self.lock = threading.Lock()
        realtime.setDaemon(True)
        realtime.start()
    def tw_stock_tool_label(self,*args):
        tk.Label(self.window,text="股票代號:").place(x=args[0],y=args[1])
    def tw_stock_tool_entry(self,*args):
        self.var = tk.StringVar()
        tk.Entry(self.window,textvariable=self.var).place(x=args[0],y=args[1])#.pack(side='top',ipadx=10)
    def tw_stock_tool_button_stock_list(self,*args):
    	tk.Button(self.window,text=args[0],command=self.tw_stock_tool_setting_window).place(x=args[1],y=args[2],height=20)
    def tw_stock_tool_setting_window(self):
    	self.app.attributes("-disabled",1)
    	stock_list_window = tk.Toplevel(self.window)
    	stock_list_window.title("Options")
    	stock_list_window.geometry("280x250")
    	### variable ###
    	entry_stock_id = tk.StringVar()
    	### stock id list window object ###
    	self.setting_entry = tk.Entry(stock_list_window,textvariable=entry_stock_id,width=30)
    	self.stock_id_list_box = tk.Listbox(stock_list_window,height=10,width=30,selectmode=tk.EXTENDED)
    	tk.Button(stock_list_window,text="join",height=1,command=lambda:self.tw_stock_tool_insert_stock_id_to_list(entry_stock_id)).place(x=230,y=10)
    	tk.Button(stock_list_window,text="enter",height=1,command=lambda:self.tw_stock_tool_setting_button_check(stock_list_window)).place(x=180,y=220,width=40)
    	tk.Button(stock_list_window,text="cancel",height=1,command=lambda:self._on_close_stock_list(stock_list_window)).place(x=230,y=220,width=40)
    	tk.Button(stock_list_window,text="delete",height=1,command=self.tw_stock_tool_setting_button_delete).place(x=230,y=40,width=40)
    	stock_list_window.focus()
    	self.stock_id_list_box.place(x=10,y=40)
    	self.setting_entry.place(x=10,y=10,height=25)
    	self._load_stock_id_setting()
    	stock_list_window.protocol("WM_DELETE_WINDOW",lambda:self._on_close_stock_list(stock_list_window))
    def _load_stock_id_setting(self):
    	stock_id = self.tw_stock_setting.Setting_load_all_items(self.tw_stock_setting.section_name)
    	for id in range(len(stock_id)):
    		self.stock_id_list_box.insert(tk.END,stock_id[id][0])
    def tw_stock_tool_setting_button_delete(self):
    	index = self.stock_id_list_box.curselection()
    	items = self.tw_stock_setting.Setting_load_all_items(self.tw_stock_setting.section_name)
    	stock_id = self.stock_id_list_box.get(index)
    	self.stock_id_list_box.delete(index)
    	self.tw_stock_setting.Setting_config_del(self.tw_stock_setting.section_name,stock_id)
    def tw_stock_tool_setting_button_check(self,stock_list_window):
    	index = self.stock_id_list_box.curselection()
    	stock_id = self.stock_id_list_box.get(index)
    	self.var.set(stock_id)
    	self._on_close_stock_list(stock_list_window)
    def tw_stock_tool_insert_stock_id_to_list(self,entry_stock_id):
    	self.stock_id_list_box.insert(tk.END,entry_stock_id.get())
    	self.tw_stock_setting.Setting_config_set(self.tw_stock_setting.section_name,entry_stock_id.get(),entry_stock_id.get())
    	self.setting_entry.delete(0,'end')
    def tw_stock_tool_button(self,*args):
        bt = tk.Button(self.window,text="show picture",width=15,command=self.tw_stock_tool_check_get).place(x=args[0],y=args[1])#.pack(side='left')
    def _on_close_stock_list(self,stock_list_window):
    	self.app.attributes("-disabled",0)
    	stock_list_window.destroy()
    def tw_stock_tool_load_stock_table(self,*args):
        bt = tk.Button(self.window,text="load file",command=self.tw_stock_tool_tables_window).place(x=args[0],y=args[1])#.pack(side='right')
    def tw_stock_tool_get_buy_sell_info(self,*args):
        bt = tk.Button(self.window,text='TPEx/TWSE',width=15,command=self.tw_stock_tool_TPEx_TWSE_info).place(x=args[0],y=args[1])
    def tw_stock_tool_realtime_button(self,*args):
        self.realtim_text = tk.StringVar()
        self.realtim_text.set("real time start")
        bt = tk.Button(self.window,text="real time",textvariable=self.realtim_text,width=15,command=self.tw_stock_tool_start).place(x=args[0],y=args[1])#.pack(side='left')
    def tw_stock_tool_start(self):
        self.realtime_id = self.var.get()
        if self.flag_items[Flags.REALTIME_LOOP.value] == True:
            self.flag_items[Flags.REALTIME_LOOP.value] = False
            self.realtim_text.set("real time start")
        elif self.flag_items[Flags.REALTIME_LOOP.value] == False:
            self.flag_items[Flags.REALTIME_LOOP.value] = True   
            self.flag_items[Flags.INIT_FIG.value] = False
            self.realtim_text.set("running")
        if not self.event.is_set():
            self.event.set()
    def tw_stock_tool_realtime(self):
        self.event.wait()
        while self.flag_items[Flags.REALTIME_START.value]:
            while self.flag_items[Flags.REALTIME_LOOP.value]:
                try:
                    self.lock.acquire()
                    result = self.tw_stock_analytics.load_stock_realtime(self.realtime_id,self.check_var3.get())
                    self.lock.release()
                    self.tw_stock_tool_all_info(result)
                    self.Tab.insert(tk.END,"委託買價"+str(result["委託買價"][1])+'\n')
                    self.Tab.insert(tk.END,"委託買量"+str(result["委託買量"][1])+'\n')
                    self.Tab.insert(tk.END,"委託賣價"+str(result["委託賣價"][1])+'\n')
                    self.Tab.insert(tk.END,"委託賣量"+str(result["委託賣量"][1])+'\n')
                    self.Tab.insert(tk.END,"成交量"+str(result["成交量"][1])+'\n')
                    if self.flag_items[Flags.TEXT_STUCK.value] == False:
                        self.Tab.see(tk.END)
                        self.Tab1.see(tk.END)
                    time.sleep(1)
                    if self.flag_items[Flags.REALTIME_LOOP.value] == False:
                        plt.show()
                        plt.close("all")
                except Exception as e:
                    sys_debug_info(e)
            time.sleep(0.1)
    def tw_stock_tool_tdcc_search(self,*args):
        bt = tk.Button(self.window,text="TDCC結算",width=11,command=lambda:\
                       TDCC_load_stock_data(self.var.get(),self.check_var1.get(),self.check_var2.get())).place(x=args[0],y=args[1])
    def tw_stock_tool_bestfourpoint(self,*args):
        bt = tk.Button(self.window,text="best four buy",command=lambda:self.tw_stock_tool_treeview(self.var.get())).place(x=args[0],y=args[1])#.pack(side='left')
    def tw_stock_tool_bestfourpoint_get(self,stock_id):
        print(self.var.get())
        if self.var.get() == "":
            self.merge_best_but_sell = self.tw_stock_analytics.load_stock_BestFourPoint(stock_id)
            return
        stock_id = twstock.Stock(self.var.get())
        self.merge_best_but_sell = self.tw_stock_analytics.load_stock_BestFourPoint(stock_id)
        print(self.merge_best_but_sell)
    def tw_stock_tool_tables_window(self):
        self.tw_stock_tool_stock_tables()
    def tw_stock_tool_treeview_preview(self,*args):
        self.index = ['1','2','3','4','5','6','7','8']
        frame_treeview = tk.Frame(self.window)
        self.tree = ttk.Treeview(frame_treeview,selectmode='browse')#.place(x=20,y=350)
        vsb = ttk.Scrollbar(frame_treeview, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_treeview, orient="horizontal", command=self.tree.xview)
        self.tree["columns"] = self.index
        print(self.index[0])
        for x in range(0,4):
            self.tree.heading(self.index[x],text=list(BEST_BUY.keys())[x])
        for x in range(0,4):
            self.tree.heading(self.index[x+4],text=list(BEST_SELL.keys())[x])
        self.tree.column("#0", width=0,stretch=True)
        #### setting index width ####
        self.tree.column(self.index[0],width=100,stretch=False)
        self.tree.column(self.index[1],width=80,stretch=False)
        self.tree.column(self.index[2],width=120,stretch=False)
        self.tree.column(self.index[3],width=120,stretch=False)
        self.tree.column(self.index[4],width=60,stretch=False)
        self.tree.column(self.index[5],width=60,stretch=False)
        self.tree.column(self.index[6],width=120,stretch=False)
        self.tree.column(self.index[7],width=120,stretch=False)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        frame_treeview.grid_rowconfigure(0, weight=1)
        self.tree.grid(row=0, column=0,sticky='NSEW')
        vsb.grid(column=1, row=0,sticky='ns')
        hsb.grid(column=0, row=1,sticky='ew')
        frame_treeview.place(x=args[0],y=args[1])
    def tw_stock_tool_treeview(self,stock_sid):
        stock = self.tw_stock_analytics.load_stock_number(str(stock_sid))
        if stock == False:
            return
        self.tw_stock_tool_bestfourpoint_get(stock)
        self.tree.insert('',0,text=stock.sid,values=self.merge_best_but_sell.values())
    def tw_stock_tool_date_entry(self,*args):
        self.TPEx_TWSE = tk.StringVar()
        tk.Entry(self.window,width=8,textvariable=self.TPEx_TWSE).place(x=args[0],y=args[1])
        tk.Label(self.window,text='填入日期').place(x=args[2],y=args[3])
        tk.Label(self.window,text='ex:110/11/01').place(x=args[4],y=args[5])
    def tw_stock_tool_check_get(self):
        line,bar = self.check_var1.get(),self.check_var2.get()
        if line == True:
            self.tw_stock_analytics.load_stock_history_data(self.var.get(),2021,8)
        if bar == True:
            self.tw_stock_analytics.load_stock_history_transaction(self.var.get())
        if (line == False and bar == False):
            tk.messagebox.showinfo('FYI','please selection checkbutton')
    def tw_stock_tool_check_button(self,*args):
        self.check_var1 = tk.BooleanVar()
        self.check_var2 = tk.BooleanVar()
        self.check_var3 = tk.BooleanVar()
        self.C1 = tk.Checkbutton(self.window,text="line_graph",variable=self.check_var1,onvalue=1,offvalue=0).place(x=args[0],y=args[1])
        self.C2 = tk.Checkbutton(self.window,text="transaction",variable=self.check_var2,onvalue=1,offvalue=0).place(x=args[2],y=args[3])
        self.C3 = tk.Checkbutton(self.window,text="realtime bar",variable=self.check_var3,onvalue=1,offvalue=0).place(x=args[4],y=args[5])
    def tw_stock_tool_check_button_date(self,*args):
        self.Day_check = tk.BooleanVar()
        self.Week_check = tk.BooleanVar()
        self.Month_check = tk.BooleanVar()
        tk.Checkbutton(self.window,text="Day",variable=self.Day_check,onvalue=1,offvalue=0).place(x=args[0],y=args[1])
        tk.Checkbutton(self.window,text="Week",variable=self.Week_check,onvalue=1,offvalue=0).place(x=args[2],y=args[3])
        tk.Checkbutton(self.window,text="Month",variable=self.Month_check,onvalue=1,offvalue=0).place(x=args[4],y=args[5])
    def tw_stock_tool_open_file(self):
        file_path = filedialog.askopenfilename(title='開啟xlsx檔案', filetypes=[('xlsx', '*.xlsx')])
        return file_path
    def tw_stock_tool_stock_tables(self):
        file_path = self.tw_stock_tool_open_file()
        stock_sid = load_stock_tables(file_path)
        for x in range(int(self.first_num.get()),int(self.end_num.get())):
            self.tw_stock_tool_treeview(stock_sid[x])
    def tw_stock_tool_range_entry(self,*args):
        self.first_num = tk.StringVar()
        self.end_num = tk.StringVar()
        tk.Entry(self.window,textvariable=self.first_num,width=5).place(x=args[0],y=args[1])
        tk.Entry(self.window,textvariable=self.end_num,width=5).place(x=args[2],y=args[3])
        text = tk.Label(self.window,text='--').place(x=args[4],y=args[5])
    def tw_stock_tool_notebook(self,*args):
        self.text_nb = ttk.Notebook(self.window,height=300,width=500)
        self.msg = tk.StringVar()
        self.Tab = tk.Text(self.text_nb)#,height=20,width=80)
        self.Tab1 = tk.Text(self.text_nb)
        self.Tab2 = tk.Text(self.text_nb)
        self.Tab3 = tk.Text(self.text_nb)
        self.text_nb.add(self.Tab,text='Message')
        self.text_nb.add(self.Tab1,text='All information')
        self.text_nb.add(self.Tab2,text="櫃買中心")
        self.text_nb.add(self.Tab3,text="外資買賣")
        self.text_nb.bind('<<NotebookTabChanged>>',self.tw_stock_tool_nb_item_index)
        self.text_nb.place(x=args[0],y=args[1])
    def tw_stock_tool_nb_item_index(self,event):
        index = self.text_nb.index(self.text_nb.select())
        if index == 0:
            scrollbar = ttk.Scrollbar(self.Tab,command=self.Tab.yview)
            scrollbar.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            scrollbar.bind("<Button-1>",self._button_1_stop)
            scrollbar.bind("<ButtonRelease-1>",self._button_release_1_start)
            self.Tab['yscrollcommand'] = scrollbar.set
        elif index == 1:
            scrollbar1 = ttk.Scrollbar(self.Tab1,command=self.Tab1.yview)
            scrollbar1.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            scrollbar1.bind("<Button-1>",self._button_1_stop)
            scrollbar1.bind("<ButtonRelease-1>",self._button_release_1_start)
            self.Tab1['yscrollcommand'] = scrollbar1.set
        elif index == 2:
            scrollbar2 = ttk.Scrollbar(self.Tab2,command=self.Tab2.yview)
            scrollbar2.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            self.Tab2['yscrollcommand'] = scrollbar2.set
        elif index == 3:
            scrollbar3 = ttk.Scrollbar(self.Tab3,command=self.Tab3.yview)
            scrollbar3.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            self.Tab3['yscrollcommand'] = scrollbar3.set
    def _button_1_stop(self,event):
        if self.flag_items[Flags.TEXT_STUCK.value] == False:
            self.flag_items[Flags.TEXT_STUCK.value] = True
    def _button_release_1_start(self,event):
        if self.flag_items[Flags.TEXT_STUCK.value] == True:
            self.flag_items[Flags.TEXT_STUCK.value] = False
    def tw_stock_tool_all_info(self,result):
        try:
            self.Tab1.insert(tk.END,str(result.iloc[0])+'\n')
            self.Tab1.insert(tk.END,str((result["委託賣價"][0])[0]+'\n'))
        except Exception as e:
            sys_debug_info(e)
    def tw_stock_tool_TPEx_TWSE_info(self):
        self.tw_stock_tool_TPEx_info()
        self.tw_stock_tool_TWSE_info()
    def tw_stock_tool_TPEx_info(self):
        if self.Day_check.get() == True:
            table = TPEx_load_stock_info(self.TPEx_TWSE.get(),period='D')
        elif self.Week_check.get() == True:
            table = TPEx_load_stock_info(self.TPEx_TWSE.get(),period='W')
        elif self.Month_check.get() == True:
            table = TPEx_load_stock_info(self.TPEx_TWSE.get(),period='M')
        index = self.TPEx_TWSE_listbox.curselection()
        table[self.TPEx_TWSE_listbox.get(index)] = table[self.TPEx_TWSE_listbox.get(index)].astype(float)
        table.sort_values(by=[self.TPEx_TWSE_listbox.get(index)],ascending=False,inplace=True)
        try:
            for x,y in zip(table[self.TPEx_TWSE_listbox.get(index)],range(int(self.rank.get()))):
                self.Tab2.insert(tk.END,"股號:{:5},名稱:{:5},買超:{:5}".format(table['代號代號'].iat[y]\
                                                 ,table['名稱名稱'].iat[y],round(x/1000)) + '\n')
            self.Tab2.insert(tk.END,'-------------------------------------'+'\n')
            for x,y in zip(table[self.TPEx_TWSE_listbox.get(index)].iloc[::-1],range(1,int(self.rank.get())+1)):
                self.Tab2.insert(tk.END,"股號:{:5},名稱:{:5},賣超:{:5}".format(table['代號代號'].iat[-y]\
                                                 ,table['名稱名稱'].iat[-y],round(x/1000)) + '\n')
                self.Tab2.see(tk.END)
            self.Tab2.insert(tk.END,'-------------------------------------'+'\n')
            if self.var.get() != "":
                self.Tab1.insert(tk.END,(table.loc[table['代號代號'] == self.var.get()]))
                self.Tab1.see(tk.END)
                self.Tab1.insert(tk.END,'-------------------------------------'+'\n')
                self.Tab2.insert(tk.END,(table.loc[table['代號代號'] == self.var.get()])[self.TPEx_TWSE_listbox.get(index)] )
        except:
            pass
    def tw_stock_tool_TWSE_info(self):
        if self.TPEx_TWSE.get().startswith("1"):
            tmp = self.TPEx_TWSE.get().replace(self.TPEx_TWSE.get()[0:3],str(int(self.TPEx_TWSE.get()[0:3])+1911))
            date_tmp = pd.to_datetime(tmp,format='%Y/%m/%d')
            date = datetime.date(date_tmp).strftime("%Y%m%d")
        table = TWSE_load_stock_info(date)
        index = self.TPEx_TWSE_listbox.curselection()
        table[self.TPEx_TWSE_listbox.get(index)] = table[self.TPEx_TWSE_listbox.get(index)].astype(float)
        table.sort_values(by=[self.TPEx_TWSE_listbox.get(index)],ascending=False,inplace=True) 
        try:
            for x,y in zip(table[self.TPEx_TWSE_listbox.get(index)],range(int(self.rank.get()))):
                self.Tab3.insert(tk.END,"股號:{:5},名稱:{:5},買超:{:5}".format(table['證券代號'].iat[y]\
                                                 ,table['證券名稱'].iat[y],round(x/1000)) + '\n')
            self.Tab3.insert(tk.END,'-------------------------------------'+'\n')
            for x,y in zip(table[self.TPEx_TWSE_listbox.get(index)].iloc[::-1],range(1,int(self.rank.get())+1)):
                self.Tab3.insert(tk.END,"股號:{:5},名稱:{:5},賣超:{:5}".format(table['證券代號'].iat[-y]\
                                                 ,table['證券名稱'].iat[-y],round(x/1000)) + '\n')
                self.Tab3.see(tk.END)
            self.Tab3.insert(tk.END,'-------------------------------------'+'\n')
            if self.var.get() != "":
                self.Tab1.insert(tk.END,(table.loc[table['證券代號'] == self.var.get()]))
                self.Tab1.see(tk.END)
                self.Tab1.insert(tk.END,'-------------------------------------'+'\n')
                self.Tab3.insert(tk.END,(table.loc[table['證券代號'] == self.var.get()])[self.TPEx_TWSE_listbox.get(index)] )

        except:
            pass
    def tw_stock_tool_TPEx_TWSE_check_button(self,*args):
        frame_lt = tk.Frame(self.window)
        scrollbar = tk.Scrollbar(frame_lt)
        self.TPEx_TWSE_listbox = tk.Listbox(frame_lt,height=3,selectmode=tk.EXTENDED)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.TPEx_TWSE_listbox.pack(side=tk.LEFT,fill=tk.BOTH)
        for i in range(len(TPEx)):
            self.TPEx_TWSE_listbox.insert(tk.END,TPEx[i])
        self.TPEx_TWSE_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.TPEx_TWSE_listbox.yview)
        frame_lt.place(x=args[0],y=args[1])
    def tw_stock_tool_rank_entry(self,*args):
        self.rank = tk.StringVar()
        tk.Entry(self.window,width=5,textvariable=self.rank).place(x=args[0],y=args[1])
        tk.Label(self.window,text='買賣超前:').place(x=args[2],y=args[3])
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.flag_items[Flags.REALTIME_START.value] == True:
                self.flag_items[Flags.REALTIME_LOOP.value] = False
            if self.flag_items[Flags.REALTIME_START.value] == True:
                self.flag_items[Flags.REALTIME_LOOP.value] = False
            self.event.clear()
            self.app.destroy()
            


        

def run():
    window = tk.Tk()
    stock_app = tw_stock_tool(window)
    window.protocol("WM_DELETE_WINDOW", stock_app.on_closing)
    window.mainloop()
    try:
    	os.system("taskkill /f /im tw_stock_tool.exe")
    except Exception as e:
    	sys_debug_info(e)

if __name__=='__main__':
    run()
