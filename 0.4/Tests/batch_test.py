import pyglet
from pyglet.gl import *
from pyglet.window import key


class Window(pyglet.window.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=True,vsync=True,)
        self.batch = pyglet.graphics.Batch()
        img = pyglet.image.load('resc\palatin.png')
        self.sprite2 = pyglet.sprite.Sprite(img,100, 0,batch=self.batch)
        self.set_minimum_size(600,600)

    def on_resize(self, width, height):
        changed_width = (width-600)/600+1
        changed_height = (height-600)/600+1
        glScalef(changed_width,changed_height,1)
        print(changed_width)        

    def on_draw(self):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.clear()
        self.batch.draw()
        self.sprite2.draw()

    def on_key_press(self, KEY, modifiers):
        pass

window = Window(600,600)
pyglet.app.run()