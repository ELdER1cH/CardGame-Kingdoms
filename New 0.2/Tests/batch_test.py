import pyglet
from pyglet.gl import *

class Window(pyglet.window.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=False,vsync=True)
        self.batch = pyglet.graphics.Batch()
        img = pyglet.image.load('resc/palatin.png')
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        tex = img.get_texture() 
        tex.width = 120
        tex.height = 100
        img.save('palatin.png') 
        self.sprite = pyglet.sprite.Sprite(img,0, 0,batch=self.batch)
        self.sprite2 = pyglet.sprite.Sprite(img,100, 0,batch=self.batch)
        del self.sprite

    def on_draw(self):
        self.clear()
        self.batch.draw()

window = Window()
pyglet.app.run()