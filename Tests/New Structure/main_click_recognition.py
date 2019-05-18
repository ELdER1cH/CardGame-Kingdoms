import pyglet
from pyglet.gl import *
from random import randint
import time
from pyglet.window import key, mouse

class CardBatch(pyglet.graphics.Batch):
  def __init__(self):
    super().__init__()
    self.sprites = []

  def add(self,*args,**kwargs):
    #print()
    return super().add(*args,**kwargs)

  def get_sprite(self,x,y):
    for sprite in self.sprites:
      if sprite.in_area(x,y):
        return sprite

  def update(self,x,y):
    for sprite in self.sprites:
      sprite.update(x,y)
  
class Card(pyglet.sprite.Sprite):
  def __init__(self,img,*args,batch=None,**kwargs):
    batch.sprites.append(self)
    self.resize(img)
    super().__init__(img,*args,batch=batch,**kwargs)
    self.resize(img)

  def resize(self,img):
    val = 1 #10
    img.get_texture().width = 120/val
    img.get_texture().height = 100/val

  def in_area(self,x,y):
    mx, my = self.position
    if x >= mx and x <= mx+self.width and y >= my and y <= my+self.height:
      return True
    
    
  def update(self,x,y):
    if self.in_area(x,y):
      self.position = (self.position[0]+10,self.position[1])

class Window(pyglet.window.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.batch = CardBatch()
    img = pyglet.image.load("card_one.png")
    self.card1 = Card(img,100,110,batch=self.batch)
    self.card2 = Card(img,100,10,batch=self.batch)

    self.cal_time = 0
    pyglet.clock.schedule(self.update)
    pyglet.clock.schedule_interval(self.print_cal_time,1)

  def update(self,dt):
    pass

  def print_cal_time(self,dt):
    print("cal_time:%s sprites:%s" % (self.cal_time,len(self.batch.sprites)))

  def on_mouse_press(self,x,y,button,MOD):
    if button == mouse.LEFT:
      reference = time.time()
      self.batch.update(x,y)
      sprite_above = self.batch.get_sprite(x,y+100)
      if sprite_above != None:
        sprite_above.position = (sprite_above.position[0]+10,sprite_above.position[1])
      self.cal_time = time.time()-reference

  def on_key_press(self,KEY,MOD):
    if KEY == key.A:
      img = pyglet.image.load("card_one.png")
      for i in range(100):
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
