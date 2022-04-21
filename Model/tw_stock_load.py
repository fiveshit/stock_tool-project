
import pandas as pd
#---------------------------------------#
#Name : load_stock_tables
#Description : load StockList.xlsx to execute
#               best fourpoint function
#Input : file path
#Output : -
#Return : stock id
#description : When user press UI,view will send event to controller.
#---------------------------------------#
def load_stock_tables(file_path):
    df = pd.DataFrame(pd.read_excel(file_path))
    # delete same item from xlsx file
    try:
        stock_sid = df['證券代號'].drop_duplicates(keep='first', inplace=False).tolist()
    except:
        stock_sid = df['代號'].drop_duplicates(keep='first', inplace=False).tolist()
    #print(stock_sid[1])
    return stock_sid
