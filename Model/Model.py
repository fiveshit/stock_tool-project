import pandas as pd
#---------------------------------------#
#Name : Stock_Mode
#Description : other function interface
#Input : -
#Output : -
#Return : -
#---------------------------------------#
class Stock_Mode:
    def __init__(self):
        print("enter Model")
    def stock_mode_pd_to_datetime(self,tmp):
        return pd.to_datetime(tmp,format='%Y/%m/%d')
    
