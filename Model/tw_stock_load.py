
import pandas as pd
def load_stock_tables(file_path):
    df = pd.DataFrame(pd.read_excel(file_path))
    try:
        stock_sid = df['證券代號'].drop_duplicates(keep='first', inplace=False).tolist()
    except:
        stock_sid = df['代號'].drop_duplicates(keep='first', inplace=False).tolist()
    #print(stock_sid[1])
    return stock_sid
