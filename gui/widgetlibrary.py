import time

import pride
import pride.gui.gui as gui
import pride.gui
import pride.base as base
Instruction = pride.Instruction

import sdl2

class Attribute_Modifier_Button(gui.Button):

    defaults = {"amount" : 0,
                "method" : "",
                "target" : None}
                     
    def left_click(self, mouse):        
        instance_name, attribute = self.target
        instance = pride.objects[instance_name]        
        old_value = getattr(instance, attribute)
        new_value = getattr(old_value, self.method)(self.amount)
        setattr(instance, attribute, new_value)
        self.alert("Modified {}.{}; {}.{}({}) = {}",
                   (instance_name, attribute, old_value, 
                    self.method, self.amount, getattr(instance, attribute)),
                   level='vv')  
                    
 
class Instruction_Button(gui.Button):
    
    defaults = {"args" : tuple(),
                "kwargs" : None,
                "method" : '',
                "instance_name" : '',
                "priority" : 0.0,
                "host_info" : tuple(),
                "callback" : None}
                     
    def left_click(self, mouse):
        Instruction(self.instance_name, self.method, 
                    *self.args, **self.kwargs or {}).execute(priority=self.priority, 
                                                             host_info=self.host_info,
                                                             callback=self.callback)
                                             
    
class Method_Button(gui.Button):
        
    defaults = {"args" : tuple(),
                "kwargs" : None,
                "method" : '',
                "target" : ''}
                     
    def left_click(self, mouse):
        try:
            instance = self.target()
        except TypeError:
            instance = pride.objects[self.target]  
        getattr(instance, self.method)(*self.args, **self.kwargs or {})     
                            

class Delete_Button(Method_Button):
    
    defaults = {"pack_mode" : "horizontal",
                "text" : "delete",
                "method" : "delete"}
        
        
class Exit_Button(Delete_Button):
        
    defaults = {"text" : "exit"}
    

class Popup_Button(gui.Button):
        
    defaults = {"popup_type" : '', "_popup" : None}

    def left_click(self, mouse):
        if self._popup:
            self._popup.delete()
        elif self.popup_type:
            self.alert("Creating: {}".format(self.popup_type), level='vv')
            self._popup = self.create(self.popup_type)
        
        
class Homescreen(gui.Window):
    
    def __init__(self, **kwargs):
        super(Homescreen, self).__init__(**kwargs)
        self.create(Task_Bar, startup_components=\
                                ("pride.gui.widgetlibrary.Date_Time_Button",
                                 "pride.gui.widgetlibrary.Text_Box"))
        

class Task_Bar(gui.Container):

    defaults = {"pack_mode" : "menu_bar",
                "bound" : (0, 20)}
    
    def _set_pack_mode(self, value):
        super(Task_Bar, self)._set_pack_mode(value)
        if self.pack_mode in ("right", "left", "horizontal"):
            self._backup_w_range = self.w_range
            self.w_range = self.bound
            self.h_range = self._backup_h_range
        else:
            self._backup_h_range = self.h_range
            self.h_range = self.bound      
            try:
                self.w_range = self._backup_w_range
            except AttributeError:
                pass
    pack_mode = property(gui.Container._get_pack_mode, _set_pack_mode)
    
    def __init__(self, **kwargs):  
        parent_name = self.parent_name
        super(Task_Bar, self).__init__(**kwargs)        
        self.create(Indicator, text=parent_name)
        self.create(Delete_Button, target=parent_name)
             
 #   def pack(self, modifiers=None):

  #      super(Task_Bar, self).pack(modifiers)
        
        
class Text_Box(gui.Container):
    
    defaults = {"h" : 16,
                "pack_mode" : "horizontal",
                "allow_text_edit" : True,
                "editing" : False}
    
    def _get_editing(self):
        return self._editing
    def _set_editing(self, value):            
        self._editing = value
        if value:
            self.alert("Turning text input on", level='vv')
            sdl2.SDL_StartTextInput()
        else:
            self.alert("Disabling text input", level='vv')
            sdl2.SDL_StopTextInput()
    editing = property(_get_editing, _set_editing) 
    
    def __init__(self, **kwargs):
        super(Text_Box, self).__init__(**kwargs)
        text_box_name = self.instance_name
        self.create(Scroll_Bar, target=(text_box_name, "texture_window_x"),
                    pack_mode="bottom")         
        self.create(Scroll_Bar, target=(text_box_name, "texture_window_y"),
                    pack_mode="right")
                        
    def left_click(self, event):
        self.alert("Left click: {}".format(self.editing), level='vvv')
        self.editing = not self.editing
        
    def draw_texture(self):
        area = self.texture.area
        self.draw("fill", area, color=self.background_color)
        self.draw("rect", area, color=self.color)
        if self.text:
            self.draw("text", self.area, self.text, 
                      bg_color=self.background_color, color=self.text_color)
        
        
class Date_Time_Button(gui.Button):

    defaults = {"pack_mode" : "horizontal"}

    def __init__(self, **kwargs):
        super(Date_Time_Button, self).__init__(**kwargs)        
        update = self.update_instruction = Instruction(self.instance_name, "update_time")        
        self.update_time()        
  
    def update_time(self):
        self.text = time.asctime()     
        self.update_instruction.execute(priority=1)   
        

class Color_Palette(gui.Window):
            
    def __init__(self, **kwargs):
        super(Color_Palette, self).__init__(**kwargs)
        color_button = self.create("pride.gui.gui.Button", pack_mode="horizontal")
        slider_container = self.create("pride.gui.gui.Container", pack_mode="horizontal")
        
        button_name = color_button.instance_name
        for color in ('r', 'g', 'b'):
            slider_container.create("pride.gui.widgetlibrary.Scroll_Bar", 
                                    target=(button_name, color))
                                    
                                    
class Scroll_Bar(gui.Container):
                           
    defaults = {"pack_mode" : "right"}
    
    def __init__(self, **kwargs):
        super(Scroll_Bar, self).__init__(**kwargs)
        if self.pack_mode in ("right", "horizontal"): # horizontal packs on the left side
            self.w_range = (0, 10)
            pack_mode = "vertical"
        else:
            self.h_range = (0, 20)
            pack_mode = "horizontal"
        options = {"target" : self.target, "pack_mode" : pack_mode}
        self.create(Decrement_Button, **options)
     #   self.create(Scroll_Indicator, **options)
        self.create(Increment_Button, **options)
        
        
class Decrement_Button(Attribute_Modifier_Button):
      
    defaults = {"amount" : 10,
                "method" : "__sub__"}
        
        
class Increment_Button(Attribute_Modifier_Button):
                
    defaults = {"amount" : 10,
                "method" : "__add__"}
                    
                    
class Scroll_Indicator(gui.Button):
            
    defaults = {"movable" : True,
                "text" : ''}
                
    def pack(self, modifiers=None):
        if self.pack_mode in ("right", "horizontal"):
            width = int(self.parent.w * .8)
            self.w_range = (width, width)
        else:
            height = int(self.parent.h * .8)
            self.h_range = (height, height)
        super(Scroll_Indicator, self).pack(modifiers)
        
    def draw_texture(self):
        super(Scroll_Indicator, self).draw_texture()
        self.draw("rect", (self.w / 4, self.h / 4,
                           self.w * 3 / 4, self.h * 3 / 4), color=self.color)
                           
        
class Indicator(gui.Button):  
    
    defaults = {"pack_mode" : "horizontal",
                "h" : 16,
                "line_color" : (255, 235, 155),
                "text" : ''}
    
    def __init__(self, **kwargs):
        super(Indicator, self).__init__(**kwargs)        
        text = self.text = self.text or self.parent_name
        
    def draw_texture(self):
        super(Indicator, self).draw_texture()
        #x, y, w, h = self.parent.area
        
        self.draw("text", self.area, self.text, color=self.text_color, width=self.w)    
        

class Done_Button(gui.Button):
        
    def left_click(self, mouse):
        getattr(pride.objects[self.callback_owner], self.callback)()        
        
        
class Prompt(gui.Application):
        
    defaults = {"callback_owner" : '',
                "callback" : ''}
                     
    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        self.create("pride.gui.widgetlibrary.Text_Box", text=self.text,
                    allow_text_edit=False)
        self.user_text = self.create("pride.gui.widgetlibrary.Text_Box")
        self.create("pride.gui.widgetlibrary.Done_Button")
   
    def handle_input(self, user_input):
        getattr(pride.objects[self.callback_owner], self.callback)(user_input)
        
        
        