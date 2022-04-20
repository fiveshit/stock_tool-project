import sys
from traceback import extract_tb
from enum import Enum
class Setting_item(Enum):
    LOAD_SECTION = 0
    LOAD_ALL_ITEMS = 1
    CONFIG_READ = 2
    CONFIG_WRITE = 3
    CONFIG_SET = 4
    CONFIG_GET = 5
    CONFIG_DEL = 6
class Stock_item(Enum):
    STOCK_LOAD_NUMBER = 0
    STOCK_LOAD_SHOW_DATA = 1
    STOCK_LOAD_HISTORY_DATA = 2
    STOCK_LOAD_HISTORY_TRANSACTION = 3
    STOCK_LOAD_REALTIME = 4
    STOCK_LOAD_BEST_FOURPOINT = 5
class Flags(Enum):
    REALTIME_LOOP = 0
    INIT_FIG = 1
    TEXT_STUCK = 2
    REALTIME_START = 3
def sys_debug_info(e):
    error_class = e.__class__.__name__ 
    detail = e.args[0] 
    cl, exc, tb = sys.exc_info() 
    lastCallStack = extract_tb(tb)[-1] 
    fileName = lastCallStack[0] 
    lineNum = lastCallStack[1] 
    funcName = lastCallStack[2] 
    errMsg = "File \"{}\n  line {} in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)
