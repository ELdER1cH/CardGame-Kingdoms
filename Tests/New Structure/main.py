import pyglet
from pyglet.gl import *
from random import randint
import time
from pyglet.window import key

class CardBatch(pyglet.graphics.Batch):
  def __init__(self):
    super().__init__()
    self.sprites = []

  def add(self,*args,**kwargs):
    #print()
    return super().add(*args,**kwargs)

  def update(self):
    for sprite in self.sprites:
      sprite.x += randint(1,10)
      if sprite.x >= 1000:
        sprite.x = 0
  
class Card(pyglet.sprite.Sprite):
  def __init__(self,img,*args,batch=None,**kwargs):
    batch.sprites.append(self)
    self.resize(img)
    super().__init__(img,*args,batch=batch,**kwargs)
    self.resize(img)

  def resize(self,img):
    img.get_texture().width = 12
    img.get_texture().height = 10
    
  def update(self):
    self.position += 10

class Window(pyglet.window.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.batch = CardBatch()
    img = pyglet.image.load("card_one.png")
    self.card1 = Card(img,100,200,batch=self.batch)
    self.card2 = Card(img,0,0,batch=self.batch)

    pyglet.clock.schedule(self.update)
    pyglet.clock.schedule_interval(self.print_cal_time,1)

  def update(self,dt):
    reference = time.time()
    self.batch.update()
    self.cal_time = time.time()-reference

  def print_cal_time(self,dt):
    print("cal_time:%s sprites:%s" % (self.cal_time,len(self.batch.sprites)))

  def on_key_press(self,KEY,MOD):
    if KEY == key.A:
      img = pyglet.image.load("card_one.png")
      for i in range(99):
        card = Card(img,0,i*10,batch=self.batch)
    
  def on_draw(self):
    self.clear()
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    self.batch.draw()
    fps_display.draw()

if __name__ == "__main__":
  window = Window(1000,1000,"New Stucture Testing",resizable=True)
  pyglet.gl.glClearColor(255,255,255,255)
  fps_display = pyglet.window.FPSDisplay(window)
  fps_display.label.font_size = 15
  pyglet.app.run()
