import sys
from traceback import extract_tb
from enum import Enum

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
