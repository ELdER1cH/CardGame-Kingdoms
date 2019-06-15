try:
  import pyglet
  from pyglet.gl import *
  import pop_up, Batch, Cards, Card,Window
  from pyglet.window import key, mouse
  from Window import Window
  import chat_dependencies.main_chat as main_chat
  import random
except ImportError as err:
  print("couldn't load modue. %s" % (err))

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
INDENTATION_RIGHT = 2

class Startscreen(main_chat.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.pre_resize_dims = (self.width,self.height)
        self.scale_x = 1
        self.scale_y = 1
        self.startlabel = pyglet.text.Label('Start',
                          font_name='Times New Roman',
                          font_size=36,
                          x=0, y=0,
                          anchor_x='center', anchor_y='center', 
                          color = (200,200,200,0))
            
        

    def on_draw(self):
        self.clear()
        self.startlabel.draw()
        
        


    def on_resize(self,width,height):
        glScalef(1/self.scale_x,1/self.scale_y,1)
        self.scale_x = width/self.pre_resize_dims[0]
        self.scale_y = height/self.pre_resize_dims[1]
        #glScalef(self.scale_x,self.scale_y,1)
        glScalef(self.scale_x,self.scale_y,1)
        super().on_resize(width,height)