import pyglet
from pyglet.gl import *
from pyglet.window import key

class Window(pyglet.window.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=True,vsync=True)

    def on_draw(self):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.clear()
        self.batch.draw()
        self.sprite2.draw()

    def on_key_press(self, KEY, modifiers):
            if KEY == key.A:
            glScalef(2.0, 2.0, 2.0)
            Window.set_size(self,900,600)
            if KEY == key.B:
            glScalef(0.5,0.5,0.5)
            print('Hallo')
window = Window()
pyglet.app.run()