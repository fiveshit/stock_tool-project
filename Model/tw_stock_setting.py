#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import configparser
import error_msg
#---------------------------------------#
#Name : Setting
#Description : create/read/write ini file
#Input : configparser.ConfigParser()
#Output : -
#Return : -
#---------------------------------------#
class Setting():
    def __init__(self):
        #init setting.ini
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(current_path,'setting.ini')
        self.config = configparser.ConfigParser()
        self.section_name = "stock_id"
        #init section
        self.config.add_section(self.section_name)
        self.Setting_load_section()
    # load ini file sections    
    def Setting_load_section(self):
        self.Setting_config_read()
        sections = self.config.sections()
        options = self.config.options(sections[0])
        return options
    # load ini file items
    def Setting_load_all_items(self,section):
        self.Setting_config_read()
        items = self.config.items(section)
        return items
    # read ini file
    def Setting_config_read(self):
        try:
            self.config.read(self.config_path)
        except Exception as e:
            error_msg.sys_debug_info(e)
    # write ini file
    def Setting_config_write(self):
        try:
            with open(self.config_path,"w") as f:
                self.config.write(f)
        except Exception as e:
            error_msg.sys_debug_info(e)
        finally:
            f.close()
    # set data to ini file
    def Setting_config_set(self,section,items,value):
        self.config.set(section,items,value)
        self.Setting_config_write()
    # get data from ini file
    def Setting_config_get(self,section,option):
        value = self.config.get(section,option)
        return value
    # delete data from ini file
    def Setting_config_del(self,section,option):
        self.config.remove_option(section,option)
        self.Setting_config_write()
        
