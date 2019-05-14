import pyglet
from pyglet.gl import *
from pyglet.window import key


class Window(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,resizable=True,vsync=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.batch = pyglet.graphics.Batch()
        pyglet.clock.schedule(self.update)
        img = pyglet.image.load('Bomb.png')
        self.sprite2 = pyglet.sprite.Sprite(img,0, 0,batch=self.batch)
        self.pre_resize_dims = (self.width,self.height)
        
    def update(self,dt):
        pass
    
    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.batch.draw()
        
    def on_resize(self, width, height):
        scale_x = width/self.pre_resize_dims[0]
        scale_y = height/self.pre_resize_dims[1]
        print(scale_y)
        glScalef(scale_x,scale_y,1)
        super().on_resize(width, height)
        self.pre_resize_dims = (self.width,self.height)

if __name__ == '__main__':
    window = Window(120,100,"resize_test")
    glClearColor(255,255,255,255)
    pyglet.app.run()
