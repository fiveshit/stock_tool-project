# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup as bs
import tkinter as tk
import requests
import platform
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import os
import analysis
import pandas as pd
import numpy as np
from error_msg import sys_debug_info

TPEx = ["外資及陸資(不含外資自營商)買賣超股數","外資自營商買賣超股數",\
        "外資及陸資買賣超股數","投信買賣超股數","自營商(自行買賣)買賣超股數",\
        "自營商(避險)買賣超股數","自營商買賣超股數",\
        "三大法人買賣超股數合計三大法人買賣超股數合計"]

url = r"https://www.tdcc.com.tw/portal/zh/smWeb/qryStock"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
def TDCC_load_stock_date():
    res = requests.get(url,headers=headers)
    soup = bs(res.text,'html.parser')
    stock_date = []
    for element in soup.find_all('option'):
        stock_date.append(element.text)
    return stock_date
def TDCC_load_stock_data(stock_num,*graph):
    date = TDCC_load_stock_date()
    analy = analysis.analysis()
    if platform.system().lower() == 'linux':
        chrome_driver_path = r"/home/joe/chromedriver_linux64/chromedriver"
    elif platform.system().lower() == 'windows':
        chrome_driver_path = r"D:\chromedriver_win32\chromedriver"
    chrome_options = webdriver.ChromeOptions()#Options()
    #chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("headless")
    browser = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    table = browser.get(url)
    row,column = 16,5
    y = [[0 for _ in range(row)] for _ in range(column)]
    for x in range(0,5):
        number = Select(browser.find_element_by_name("scaDate"))
        number.select_by_value(date[x])
        time.sleep(1)

        browser.find_element_by_id("StockNo").clear()
        browser.find_element_by_id("StockNo").send_keys(stock_num)

        browser.find_element_by_xpath("//tr[4]//td[1]//input[1]").click()
        time.sleep(3)
        soup = bs(browser.page_source,'html.parser')
        tables = soup.find("table", class_="table").find("tbody")##.find_all("tr")
        tmp = []
        #x = [100,1000,5000,10000,50000,100000,500000]
        for tr in tables.select('tr'):
            tmp.append(tr.select('td')[2].text)
        print("item {} finish".format(x))
        list_sum = [i for i in tmp if i != '']
        print(list_sum)
        for i in range(len(list_sum)):
            y[x][i] = int((list_sum[i].replace(',', '')))#append(int((tmp[i].replace(',', ''))))
        del y[x][-1]
    if graph[0] == 1:
        analy.create_sum_line_graph(stock_num,y)
    elif graph[1] == 2:
        analy.create_bar_graph(stock_num,y)
    else:
        analy.create_bar_graph(stock_num,y) 
    browser.close()
    os.system('taskkill /im chromedriver.exe /F')
    """
0                                         nan
1                                       代號代號
2                                       名稱名稱
3                         外資及陸資(不含外資自營商)買進股數
4                         外資及陸資(不含外資自營商)賣出股數
5                        外資及陸資(不含外資自營商)買賣超股數
6                                  外資自營商買進股數
7                                  外資自營商賣出股數
8                                 外資自營商買賣超股數
9                                  外資及陸資買進股數
10                                 外資及陸資賣出股數
11                                外資及陸資買賣超股數
12                                    投信買進股數
13                                    投信賣出股數
14                                   投信買賣超股數
15                             自營商(自行買賣)買進股數
16                             自營商(自行買賣)賣出股數
17                            自營商(自行買賣)買賣超股數
18                               自營商(避險)買進股數
19                               自營商(避險)賣出股數
20                              自營商(避險)買賣超股數
21                                   自營商買進股數
22                                   自營商賣出股數
23                                  自營商買賣超股數
24                    三大法人買賣超股數合計三大法人買賣超股數合計
    """
def TPEx_load_stock_info(date,period='D'):
    TPEx_info_url = 'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=htm&se=EW&t={}&d={}&s=0,asc'.format(period,date)
    response = requests.get(TPEx_info_url)
    # dispaly all information from table 
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)
    #pd.set_option('max_colwidth',100)
    folder_name = 'TPEx'
    TPEx_folder = os.path.exists(folder_name)
    if not TPEx_folder:
        os.mkdir(folder_name)
    TPEx_file_name = '{}/TPEx_{}_{}_{}_{}.html'.format(folder_name,date[0:3],date[4:6],date[7:9],period)
    if os.path.isfile(TPEx_file_name) == False:
        with open(TPEx_file_name,'wb') as file:
            file.write(response.content[1:])
            file.close()
    try:
        with open(TPEx_file_name,'r',encoding="utf-8") as file:
            html = file.read()
        html_pd = pd.read_html(html)
        for i in html_pd:
            csv_table = pd.DataFrame(i)
            csv_table.to_csv('TPEx.csv',encoding='utf-8')
        table = pd.DataFrame(pd.read_csv("TPEx.csv",header=None))# header important
        table.drop(table.columns[0],axis=1,inplace=True) #delete don't need items
        rename_para = table.iloc[1]+table.iloc[2]
        table.drop(table.index[0:3],axis=0,inplace=True)#delete don't need items
        table.drop(table.index[-1],axis=0,inplace=True)#delete don't need items
        table.rename(columns=rename_para,inplace=True)
    except Exception as e:
        sys_debug_info(e)
        return None
    except IOError:
        tk.messagebox.showinfo('Error','Cant find TPEx file')
        return None
    else:
        file.close()
    return table
def TWSE_load_stock_info(date):
    TWSE_info_url = r"https://www.twse.com.tw/fund/T86?response=html&date={}&selectType=ALL".format(date)
    # dispaly all information from table 
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth',100)
    response = requests.get(TWSE_info_url)
    folder_name = 'TWSE'
    TWSE_folder = os.path.exists(folder_name)
    if not TWSE_folder:
        os.makedirs(folder_name)
    TWSE_file_name = '{}/TWSE_{}.html'.format(folder_name,date)
    if os.path.isfile(TWSE_file_name) == False:
        try:
            with open(TWSE_file_name,'wb') as file:
                file.write(response.content[1:])
        except Exception as e:
            sys_debug_info(e)
            return None
        else:
            file.close()
    try:
        with open(TWSE_file_name,'r',encoding="utf-8") as file:
            html = file.read()
        html_pd = pd.read_html(html)
        for i in html_pd:
            csv_table = pd.DataFrame(i)
            csv_table.to_csv('TWSE.csv',encoding='utf-8')
        table = pd.DataFrame(pd.read_csv("TWSE.csv",header=None))# header important
        rename_para = table.iloc[1]
        table.drop(table.index[0:2],axis=0,inplace=True)#delete don't need items
        table.rename(columns=rename_para,inplace=True)
        table.rename(columns={'外陸資買賣超股數(不含外資自營商)':'外資及陸資(不含外資自營商)買賣超股數',\
                          '外資自營商買賣超股數':'外資自營商買賣超股數',\
                          '投信買賣超股數':'投信買賣超股數','自營商買賣超股數(自行買賣)':'自營商(自行買賣)買賣超股數',\
                          '自營商買賣超股數(避險)':'自營商(避險)買賣超股數',\
                          '三大法人買賣超股數':'三大法人買賣超股數合計三大法人買賣超股數合計'},inplace=True)
    except Exception as e:
        sys_debug_info(e)
        return None
    except IOError:
        tk.messagebox.showinfo('Error','Cant find TWSE file')
        return None
    else:
        file.close()
    return table
    
        

