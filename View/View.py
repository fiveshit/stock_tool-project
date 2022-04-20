import time
import tkinter as tk
from tkinter import ttk
from Controller.error_msg import *
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from Controller.error_msg import sys_debug_info
from datetime import datetime

#---------------------------------------#
#Name : Stock_View
#Description : Tkinter module create UI
#Input : tkinter.Tk(),window
#Output : -
#Return : -
#description : When user press UI,view will send event to controller.
#---------------------------------------#
class Stock_View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window = self
    def tw_stock_view_init_ui(self):
        self.window.title('stock app')
        self.window.geometry('820x650')
        # sub View
        self.tw_stock_options_view = Stock_Options_View(self.window)
        #----------------------------- 
        #           create all View UI
        #-----------------------------
        self.tw_stock_view_label(10,20)
        self.tw_stock_view_entry(75,20)
        self.tw_stock_view_button_stock_list("list",230,20)
        self.tw_stock_view_check_button(75,50,75,70,175,50)
        self.tw_stock_view_button(50,100)
        self.tw_stock_view_tdcc_search(200,130)
        self.tw_stock_view_realtime_button(50,130)
        self.tw_stock_view_load_stock_table(50,160)
        self.tw_stock_view_check_button_date(50,200,100,200,160,200)
        self.tw_stock_view_bestfourpoint(200,100)
        self.tw_stock_view_range_entry(120,162,190,162,165,162)
        self.tw_stock_view_notebook(300,20)
        self.tw_stock_view_get_buy_sell_info(50,230)
        self.tw_stock_view_treeview_preview(0,350)
        self.tw_stock_view_date_entry(120,260,50,260,165,230)
        self.tw_stock_view_TPEx_TWSE_check_button(50,280)
        self.tw_stock_view_rank_entry(240,260,180,260)

    def tw_stock_view_label(self,*args):
        tk.Label(self.window,text="股票代號:").place(x=args[0],y=args[1])
    def tw_stock_view_entry(self,*args):
        self.var = tk.StringVar()
        tk.Entry(self.window,textvariable=self.var).place(x=args[0],y=args[1])#.pack(side='top',ipadx=10)
    def tw_stock_view_button_stock_list(self,*args):
        tk.Button(self.window,text=args[0],command=self.tw_stock_options_view.tw_stock_options_view_setting_window).place(x=args[1],y=args[2],height=20)
    def tw_stock_view_check_button(self,*args):
        self.check_var1 = tk.BooleanVar()
        self.check_var2 = tk.BooleanVar()
        self.check_var3 = tk.BooleanVar()
        self.C1 = tk.Checkbutton(self.window,text="line_graph",variable=self.check_var1,onvalue=1,offvalue=0).place(x=args[0],y=args[1])
        self.C2 = tk.Checkbutton(self.window,text="transaction",variable=self.check_var2,onvalue=1,offvalue=0).place(x=args[2],y=args[3])
        self.C3 = tk.Checkbutton(self.window,text="realtime bar",variable=self.check_var3,onvalue=1,offvalue=0).place(x=args[4],y=args[5])
    def tw_stock_view_button(self,*args):
        bt = tk.Button(self.window,text="show picture",width=15,command=self.tw_stock_view_check_get).place(x=args[0],y=args[1])#.pack(side='left')
    def tw_stock_view_check_get(self):
        line,bar = self.check_var1.get(),self.check_var2.get()
        if line == True:
            self.controller.tw_stock_controller_stock(Stock_item.STOCK_LOAD_HISTORY_DATA,self.var.get(),2021,8)
        if bar == True:
            self.controller.tw_stock_controller_stock(Stock_item.STOCK_LOAD_HISTORY_TRANSACTION,self.var.get())
        if (line == False and bar == False):
            tk.messagebox.showinfo('FYI','please selection checkbutton')
    def tw_stock_view_tdcc_search(self,*args):
        bt = tk.Button(self.window,text="TDCC結算",width=11,command=lambda:\
                         self.controller.tw_stock_controller_tdcc(TDCC_item.TDCC_LOAD_DATA,self.var.get(),self.check_var1.get(),self.check_var2.get())).place(x=args[0],y=args[1])
                       
    def tw_stock_view_realtime_button(self,*args):
        realtim_text = tk.StringVar()
        realtim_text.set("real time start")
        bt = tk.Button(self.window,text="real time",textvariable=realtim_text,width=15,command=lambda:self.controller.tw_stock_controller_realtime_run(self.var.get(),realtim_text)).place(x=args[0],y=args[1])#.pack(side='left')#command=self.tw_stock_tool_start
    def tw_stock_view_load_stock_table(self,*args):
        bt = tk.Button(self.window,text="load file",command=self.tw_stock_view_stock_tables).place(x=args[0],y=args[1])#.pack(side='right')
    def tw_stock_view_stock_tables(self):
        file_path = self.tw_stock_view_open_file()
        stock_sid = self.controller.tw_stock_load_data(file_path)
        for x in range(int(self.first_num.get()),int(self.end_num.get())):
            self.tw_stock_view_treeview(stock_sid[x])
    def tw_stock_view_open_file(self):
        file_path = filedialog.askopenfilename(title='開啟xlsx檔案', filetypes=[('xlsx', '*.xlsx')])
        return file_path
    def tw_stock_view_check_button_date(self,*args):
        self.Day_check = tk.BooleanVar()
        self.Week_check = tk.BooleanVar()
        self.Month_check = tk.BooleanVar()
        tk.Checkbutton(self.window,text="Day",variable=self.Day_check,onvalue=1,offvalue=0).place(x=args[0],y=args[1])
        tk.Checkbutton(self.window,text="Week",variable=self.Week_check,onvalue=1,offvalue=0).place(x=args[2],y=args[3])
        tk.Checkbutton(self.window,text="Month",variable=self.Month_check,onvalue=1,offvalue=0).place(x=args[4],y=args[5])
    def tw_stock_view_bestfourpoint(self,*args):
        bt = tk.Button(self.window,text="best four buy",command=lambda:self.tw_stock_view_treeview(self.var.get())).place(x=args[0],y=args[1])#.pack(side='left') #command=lambda:self.tw_stock_tool_treeview(self.var.get())
    def tw_stock_view_treeview(self,stock_sid):
        
        stock = self.controller.tw_stock_controller_stock(Stock_item.STOCK_LOAD_NUMBER,str(stock_sid))
        if stock == False:
            return
        merge_best_but_sell = self.controller.tw_stock_controller_stock(Stock_item.STOCK_LOAD_BEST_FOURPOINT,stock,self.var.get())
        
        
        self.tree.insert('',0,text=stock.sid,values=merge_best_but_sell.values())
    def tw_stock_view_range_entry(self,*args):
        self.first_num = tk.StringVar()
        self.end_num = tk.StringVar()
        tk.Entry(self.window,textvariable=self.first_num,width=5).place(x=args[0],y=args[1])
        tk.Entry(self.window,textvariable=self.end_num,width=5).place(x=args[2],y=args[3])
        text = tk.Label(self.window,text='--').place(x=args[4],y=args[5])
    def tw_stock_view_notebook(self,*args):
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
        self.text_nb.bind('<<NotebookTabChanged>>',self.tw_stock_view_nb_item_index)
        self.text_nb.place(x=args[0],y=args[1])
    def tw_stock_view_nb_item_index(self,event):
        index = self.text_nb.index(self.text_nb.select())
        if index == 0:
            scrollbar = ttk.Scrollbar(self.Tab,command=self.Tab.yview)
            scrollbar.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            scrollbar.bind("<Button-1>",self.controller.tw_stock_controller_stop)
            scrollbar.bind("<ButtonRelease-1>",self.controller.tw_stock_controller_start)
            self.Tab['yscrollcommand'] = scrollbar.set
        elif index == 1:
            scrollbar1 = ttk.Scrollbar(self.Tab1,command=self.Tab1.yview)
            scrollbar1.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            scrollbar1.bind("<Button-1>",self.controller.tw_stock_controller_stop)
            scrollbar1.bind("<ButtonRelease-1>",self.controller.tw_stock_controller_start)
            self.Tab1['yscrollcommand'] = scrollbar1.set
        elif index == 2:
            scrollbar2 = ttk.Scrollbar(self.Tab2,command=self.Tab2.yview)
            scrollbar2.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            self.Tab2['yscrollcommand'] = scrollbar2.set
        elif index == 3:
            scrollbar3 = ttk.Scrollbar(self.Tab3,command=self.Tab3.yview)
            scrollbar3.grid(row=0, column=0,ipady=125,padx=480,sticky="nsew")
            self.Tab3['yscrollcommand'] = scrollbar3.set
    def tw_stock_view_get_buy_sell_info(self,*args):
        bt = tk.Button(self.window,text='TPEx/TWSE',width=15,command=self.tw_stock_view_TPEx_TWSE_info).place(x=args[0],y=args[1])
    def tw_stock_view_TPEx_TWSE_info(self):
        self.tw_stock_view_TPEx_info()
        self.tw_stock_view_TWSE_info()
    def tw_stock_view_TPEx_info(self):
        if self.Day_check.get() == True:
            table = self.controller.tw_stock_controller_tdcc(TDCC_item.TPEX_LOAD_INFO,self.TPEx_TWSE.get(),period='D')
        elif self.Week_check.get() == True:
            table = self.controller.tw_stock_controller_tdcc(TDCC_item.TPEX_LOAD_INFO,self.TPEx_TWSE.get(),period='W')
        elif self.Month_check.get() == True:
            table = self.controller.tw_stock_controller_tdcc(TDCC_item.TPEX_LOAD_INFO,self.TPEx_TWSE.get(),period='M')
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
    def tw_stock_view_TWSE_info(self):
        if self.TPEx_TWSE.get().startswith("1"):
            tmp = self.TPEx_TWSE.get().replace(self.TPEx_TWSE.get()[0:3],str(int(self.TPEx_TWSE.get()[0:3])+1911))
            date_tmp = self.controller.tw_stock_controller_model(tmp)
            date = datetime.date(date_tmp).strftime("%Y%m%d")
        table = self.controller.tw_stock_controller_tdcc(TDCC_item.TWSE_LOAD_INFO,date)
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
    def tw_stock_view_treeview_preview(self,*args):
        self.index = ['1','2','3','4','5','6','7','8']
        frame_treeview = tk.Frame(self.window)
        self.tree = ttk.Treeview(frame_treeview,selectmode='browse')#.place(x=20,y=350)
        vsb = ttk.Scrollbar(frame_treeview, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_treeview, orient="horizontal", command=self.tree.xview)
        self.tree["columns"] = self.index
        print(self.index[0])
        best_buy = self.controller.tw_stock_controller_BEST_BUY()
        best_sell = self.controller.tw_stock_controller_BEST_SELL()
        for x in range(0,4):
            self.tree.heading(self.index[x],text=list(best_buy.keys())[x])
        for x in range(0,4):
            self.tree.heading(self.index[x+4],text=list(best_sell.keys())[x])
        
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
    def tw_stock_view_date_entry(self,*args):
        self.TPEx_TWSE = tk.StringVar()
        tk.Entry(self.window,width=8,textvariable=self.TPEx_TWSE).place(x=args[0],y=args[1])
        tk.Label(self.window,text='填入日期').place(x=args[2],y=args[3])
        tk.Label(self.window,text='ex:110/11/01').place(x=args[4],y=args[5])
    def tw_stock_view_TPEx_TWSE_check_button(self,*args):
        frame_lt = tk.Frame(self.window)
        scrollbar = tk.Scrollbar(frame_lt)
        self.TPEx_TWSE_listbox = tk.Listbox(frame_lt,height=3,selectmode=tk.EXTENDED)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.TPEx_TWSE_listbox.pack(side=tk.LEFT,fill=tk.BOTH)
        TPEx = self.controller.tw_stock_controller_param_TPEx()
        for i in range(len(TPEx)):
            self.TPEx_TWSE_listbox.insert(tk.END,TPEx[i])
        self.TPEx_TWSE_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.TPEx_TWSE_listbox.yview)
        
        frame_lt.place(x=args[0],y=args[1])
    def tw_stock_view_rank_entry(self,*args):
        self.rank = tk.StringVar()
        tk.Entry(self.window,width=5,textvariable=self.rank).place(x=args[0],y=args[1])
        tk.Label(self.window,text='買賣超前:').place(x=args[2],y=args[3])
    def tw_stock_view_all_info(self,result):
        try:
            self.Tab1.insert(tk.END,str(result.iloc[0])+'\n')
            self.Tab1.insert(tk.END,str((result["委託賣價"][0])[0]+'\n'))
        except Exception as e:
            sys_debug_info(e)
    def tw_stock_view_realtime(self,event,lock,flag_items):
        event.wait()
        while flag_items[Flags.REALTIME_START.value]:
            while flag_items[Flags.REALTIME_LOOP.value]:
                try:
                    lock.acquire()
                    result = self.controller.tw_stock_controller_stock(Stock_item.STOCK_LOAD_REALTIME,self.check_var3.get())
                    
                    lock.release()
                    self.tw_stock_view_all_info(result)
                    self.Tab.insert(tk.END,"委託買價"+str(result["委託買價"][1])+'\n')
                    self.Tab.insert(tk.END,"委託買量"+str(result["委託買量"][1])+'\n')
                    self.Tab.insert(tk.END,"委託賣價"+str(result["委託賣價"][1])+'\n')
                    self.Tab.insert(tk.END,"委託賣量"+str(result["委託賣量"][1])+'\n')
                    self.Tab.insert(tk.END,"成交量"+str(result["成交量"][1])+'\n')
                    if flag_items[Flags.TEXT_STUCK.value] == False:
                        self.Tab.see(tk.END)
                        self.Tab1.see(tk.END)
                    time.sleep(1)
                    if flag_items[Flags.REALTIME_LOOP.value] == False:
                        plt.show()
                        plt.close("all")
                except Exception as e:
                    sys_debug_info(e)
            time.sleep(0.1)
    #----------------------------------------------------------------------
    #                      View executes functions from Conrtoller to Model
    #----------------------------------------------------------------------
    def tw_stock_view_set_to_controller(self,controller):
        self.controller = controller
#---------------------------------------#
#Name : Stock_Options_View
#Description : Tkinter module Options UI
#Input : tkinter.Tk(),window
#Output : -
#Return : -
#description : When user press options UII,view will send event to controller.
#---------------------------------------#
class Stock_Options_View(Stock_View):
    def __init__(self,window):
        self.window = window
    def tw_stock_options_view_setting_window(self):
        self.window.attributes("-disabled",1)
        stock_list_window = tk.Toplevel(self.window)
        stock_list_window.title("Options")
        stock_list_window.geometry("280x250")
    	### variable ###
        entry_stock_id = tk.StringVar()
    	### stock id list window object ###
        self.setting_entry = tk.Entry(stock_list_window,textvariable=entry_stock_id,width=30)
        self.stock_id_list_box = tk.Listbox(stock_list_window,height=10,width=30,selectmode=tk.EXTENDED)
        tk.Button(stock_list_window,text="join",height=1,command=lambda:self.tw_stock_options_view_insert_stock_id_to_list(entry_stock_id)).place(x=230,y=10)
        tk.Button(stock_list_window,text="enter",height=1,command=lambda:self.tw_stock_options_view_setting_button_check(stock_list_window)).place(x=180,y=220,width=40)
        tk.Button(stock_list_window,text="cancel",height=1,command=lambda:self.tw_stock_options_view_on_close_stock_list(stock_list_window)).place(x=230,y=220,width=40)
        tk.Button(stock_list_window,text="delete",height=1,command=self.tw_stock_options_view_tool_setting_button_delete).place(x=230,y=40,width=40)
        stock_list_window.focus()
        self.stock_id_list_box.place(x=10,y=40)
        self.setting_entry.place(x=10,y=10,height=25)
        self._load_stock_id_setting()
        stock_list_window.protocol("WM_DELETE_WINDOW",lambda:self.tw_stock_options_view_on_close_stock_list(stock_list_window))
    def _load_stock_id_setting(self):
    	stock_id = self.controller.tw_stock_controller_setting(Setting_item.LOAD_ALL_ITEMS)#self.tw_stock_setting.Setting_load_all_items(self.tw_stock_setting.section_name)
    	for id in range(len(stock_id)):
    		self.stock_id_list_box.insert(tk.END,stock_id[id][0])
    def tw_stock_options_view_insert_stock_id_to_list(self,entry_stock_id):
        self.stock_id_list_box.insert(tk.END,entry_stock_id.get())
        self.controller.tw_stock_controller_setting(Setting_item.CONFIG_SET,entry_stock_id.get(),entry_stock_id.get())#self.tw_stock_setting.Setting_config_set(self.tw_stock_setting.section_name,entry_stock_id.get(),entry_stock_id.get())
        self.setting_entry.delete(0,'end')
    def tw_stock_options_view_setting_button_check(self,stock_list_window):
    	index = self.stock_id_list_box.curselection()
    	stock_id = self.stock_id_list_box.get(index)
    	self.var.set(stock_id)
    	self.tw_stock_options_view_on_close_stock_list(stock_list_window)
    def tw_stock_options_view_on_close_stock_list(self,stock_list_window):
    	self.window.attributes("-disabled",0)
    	stock_list_window.destroy()
    def tw_stock_options_view_tool_setting_button_delete(self):
    	index = self.stock_id_list_box.curselection()
    	self.controller.tw_stock_controller_setting(Setting_item.LOAD_ALL_ITEMS)#items = self.tw_stock_setting.Setting_load_all_items(self.tw_stock_setting.section_name)
    	stock_id = self.stock_id_list_box.get(index)
    	self.stock_id_list_box.destock_id_list_boxlete(index)
    	self.controller.tw_stock_controller_setting(Setting_item.CONFIG_DEL,stock_id)#self.tw_stock_setting.Setting_config_del(self.tw_stock_setting.section_name,stock_id)
    
        
