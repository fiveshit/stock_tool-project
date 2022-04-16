from error_msg import Setting_item
from View.View import Stock_View
from Model.Model import Stock_Mode
from Model.tw_stock_setting import Setting


class Stock_Controller:
    def __init__(self):
        self.model = Stock_Mode()
        self.view = Stock_View()
        self.setting = Setting()
        self.view.tw_stock_view_set_to_controller(self)
        self.view.tw_stock_view_init_ui()
    def run(self):
        self.view.window.mainloop()
#    LOAD_SECTION = 0
#    LOAD_ALL_ITEMS = 1
#    CONFIG_READ = 2
#    CONFIG_WRITE = 3
#    CONFIG_SET = 4
#    CONFIG_GET = 5
#    CONFIG_DEL = 6
    def tw_stock_controller_setting(self,item,*args):
        if item == LOAD_SECTION:
            print("do load section")
        elif item == LOAD_ALL_ITEMS:
            return self.model.Setting_load_all_items(self.setting.section_name)  
        elif item == CONFIG_READ:
            print("do config read")
        elif item == CONFIG_WRITE:
            print("do config write")
        elif item == CONFIG_SET:
            self.setting.Setting_config_set(self.setting.section_name,args[0],args[1])
        elif item == CONFIG_GET:
            print("do config get")
        elif item == CONFIG_DEL:
            self.setting.Setting_config_del(self.setting.section_name,args[0])
            print("do config delete")
        
        











