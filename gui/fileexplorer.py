import collections
import os

import pride.gui.widgetlibrary
import pride.gui.gui

class File_Explorer(pride.gui.gui.Application):
    
    defaults = {"current_working_directory" : '.'}
                                     
    def __init__(self, **kwargs):
        self.file_details = collections.defaultdict(lambda: [])        
        super(File_Explorer, self).__init__(**kwargs) 
        current_directory = self.current_working_directory
        for filename in os.listdir(current_directory):
            full_name = os.path.join(current_directory, filename)
            if os.path.isfile(full_name):
                self.file_details["Name"].append(filename)
                self.file_details["Type"].append(os.path.split(filename)[-1][1:]) # 1: removes the dot
                self.file_details["Size"].append(os.path.getsize(full_name))
                
                file_information = os.stat(full_name)
                self.file_details["Date_Created"].append(file_information.st_ctime)
                self.file_details["Date_Modified"].append(file_information.st_mtime)
                
        self.create(Navigation_Bar)
        self.create(Info_Bar, pack_mode="bottom")
        self.create(Directory_Viewer)        
        

class Navigation_Bar(pride.gui.gui.Container):
            
    defaults = {"pack_mode" : "top", "h_range" : (0, 20)}
    
    def __init__(self, **kwargs):
        super(Navigation_Bar, self).__init__(**kwargs)
        self.create(Back_Button)
        self.create(Forward_Button)
        self.create(History_Dropdown)
        self.create(Ascend_Button)
        self.create(Search_Bar, 
                    callback=(self.parent_application.instance_name + "->Directory_Viewer",
                              "handle_input"))
        
   
class Back_Button(pride.gui.widgetlibrary.Method_Button):
    
    defaults = {"text" : "<-", "method" : "back", "pack_mode" : "left",}
       
    
class Forward_Button(pride.gui.widgetlibrary.Method_Button):
        
    defaults = {"text" : "->", "method" : "forward", "pack_mode" : "left"}
       

class History_Dropdown(pride.gui.widgetlibrary.Popup_Button):
        
    defaults = {"popup_type" : "pride.gui.fileexplorer.Directory_History",
                "pack_mode" : "left", "text" : "history"}
    flags = {"scale_to_text" : True}
    

class Ascend_Button(pride.gui.widgetlibrary.Method_Button):
            
    defaults = {"method" : "ascend_directory", "text" : "..", "pack_mode" : "left"}    
      
    
class Search_Bar(pride.gui.widgetlibrary.Prompt): 

    defaults = {"pack_mode" : "left"}        
    
        
class Places_Bar(pride.gui.gui.Container):
            
    defaults = {"pack_mode" : "left"}
    
    def __init__(self, **kwargs):
        super(Places_Bar, self).__init__(**kwargs)
        #self.create(Lru_Directory_Dropdown)
        #self.create(Remote_Host_Dropdown)
        

class Info_Bar(pride.gui.gui.Container):
            
    defaults = {"pack_mode" : "bottom", "h_range" : (0, 20)}
    
    def __init__(self, **kwargs):
        super(Info_Bar, self).__init__(**kwargs)
        #self.create(Item_Count_Indicator
        #self.create(Selection_Count_Indicator)
        #self.create(File_Size_Indicator)
        
        
class Directory_Viewer(pride.gui.gui.Window):
        
    defaults = {"pack_mode" : "main"}
    
    def __init__(self, **kwargs):
        super(Directory_Viewer, self).__init__(**kwargs)
        self.create(Places_Bar)
        self.create(Column_Viewer)
    
    
class Column_Viewer(pride.gui.gui.Window):
        
    defaults = {"default_columns" : ("Type", "Name", "Size", 
                                     "Date_Created", "Date_Modified"),
                "pack_mode" : "right", "sorted_by" : "Type"}
                
    def __init__(self, **kwargs):
        super(Column_Viewer, self).__init__(**kwargs)
        for column_name in self.default_columns:
            container = self.create("pride.gui.gui.Container", pack_mode="left")
            container.create(Sort_Button, text=column_name)
            if column_name == "Name":
                button_type = Filename_Button
            else:
                button_type = "pride.gui.widgetlibrary.Text_Box"
                    
          #  for file_detail in self.parent_application.file_details[column_name]:
          #      container.create(button_type, text=str(file_detail), pack_mode="top")
            
            
class Sort_Button(pride.gui.gui.Button):
                
    def left_click(self, mouse):
        self.parent.sorted_by = self.text
        
        
class Filename_Button(pride.gui.gui.Button):
            
    def left_click(self, mouse):
        if not self.selected:
            self.selected = True
        else:
            self.allow_text_edit = True