# tw-stock-project
# python version 
3.8.10
# pyinstaller 打包成 exe 執行檔如下指令
# 切換到檔案目錄下 (建議目錄下含有"新版工模指令對應表.xlsx"此檔案，會一併包入)
pyinstaller -w main.py -p Model/Model.py -p Model/tw_stock.py -p Model/tw_stock_load.py -p Model/tw_stock_setting.py -p Model/tw_stock_tdcc.py -p View/View.py -p Controller/Controller.py -p Controller/error_msg.py --add-data ..\..\Lib\site-packages\twstock\codes;twstock\codes

# 引用Lib
# 可用 pip3 下載所需要用到的 Lib
pip3 install tk
pip3 install time
pip3 install pandas
pip3 install numpy
pip3 install datetime
pip3 install matplotlib
pip3 install thread6
pip3 install chardet
pip3 install enum
pip3 install configparser
pip3 install traceback
pip3 install requests
pip3 install platform
pip3 install selenium
pip3 install bs4
pip3 install lxml
pip3 install twstock
# 編譯
1. 使用 IDE 編譯
2. python main.py

![Image test](https://github.com/fiveshit/stock_tool-project/blob/main/tool_ui.PNG)
