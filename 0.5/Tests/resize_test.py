import pyglet
from pyglet.gl import *
from pyglet.window import key

class Window(pyglet.window.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=True,vsync=True)
        label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=Window.width, y=Window.height,
                          anchor_x='center', anchor_y='center')

    def on_draw(self):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.clear()
        self.label.draw()
    
    def on_resize(self, width, height):
        oldwidth = 600
        changed_width = (width-oldwidth)/oldwidth
        oldwidth = Window.get_size(self)
        print(changed_width) 

    def on_key_press(self, KEY, modifiers):
        if KEY == key.A:
            glScalef(2.0, 2.0, 2.0)
            Window.set_size(self,900,600)
        if KEY == key.B:
            glScalef(0.5,0.5,0.5)
            print('Hallo')
    
            
window = Window()
pyglet.app.run()