import pyglet
from pyglet.gl import *
from random import randint
import time
from pyglet.window import key, mouse
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)

class Cards:
  def green():
    owner = "green"
    img = pyglet.image.load('green_frame.png')#green_frame
    name = "green_frame"
    return img, owner, name

  def yellow():
    owner = "yellow"
    img = pyglet.image.load('yellow_frame.png')
    name = "yellow_frame"
    return img, owner, name

  def gray():
    owner = 'noone'
    img = pyglet.image.load('gray_frame.png')
    name = "gray_frame"
    return img, owner, name

  def castle(owner):
    owner = owner
    img = pyglet.image.load('Castle.png')
    name = "yellow_frame"
    return img, owner, name

class Card(pyglet.sprite.Sprite):
  def __init__(self,card_type,*args,batch,**kwargs):
    batch.cards.append(self)
    super().__init__(card_type[0],*args,batch=batch,**kwargs)
    self.resize()

    self.owner = card_type[1]
    self.name = card_type[2]
    
    self.attack_dmg = 10
    self.defend_dmg = 5

    self.set_dot()

  def resize(self):
    self.image.get_texture().width = SPRITE_WIDTH
    self.image.get_texture().height = SPRITE_HEIGHT
    self.w = SPRITE_WIDTH
    self.h = SPRITE_HEIGHT

  def set_dot(self):
    base = self.image.texture
    texture = pyglet.image.Texture.create(width=self.w,height=self.h)
    if self.owner == 'yellow':
      img = pyglet.image.load("yellow_dot.png").get_image_data()
      base.blit_into(img, x=0, y=0, z=0)
    elif self.owner == "green":
      img = pyglet.image.load("green_dot.png").get_image_data()
      base.blit_into(img, x=0, y=0, z=0)
  
  def in_area(self,*pos):
    mx, my = self.position
    for x,y in pos:
      if x >= mx and x <= mx+self.w and y >= my and y <= my+self.h:
        return True

  def fight(self,oppponent):
    opponent.health -= self.attack_dmg

  def defend(self,attacker):
    attacker.health -= self.defend_dmg   

  def heal(self):
    to_heal = self.batch.get_adjacent(self.position)
    for card in to_heal:
      card.health += 100
    
  def update(self,pos):
    if self.in_area((pos)):
      self.position = (self.position[0]+10,self.position[1])
      

class CardGroup:
  def __init__(self,positon,batch,*cards):
    batch.card_groups.append(self)
    self.batch = batch
    self.position = position
    self.h = 100
    self.w = 120
    self.num_cards = 0
    for card in cards:
      self.add_card(card)

  def remove_card(self):
    pass

  def add_card(self):
    pass

  def in_area(self,*pos):
    mx, my = self.position
    for x,y in pos:
      if x >= mx and x <= mx+self.w and y >= my and y <= my+self.h:
        return True      
      
class CardBatch(pyglet.graphics.Batch):      
  def __init__(self):
    super().__init__()
    self.cards = []
    self.card_groups = []
    Card(Cards.castle("yellow"),240,100,batch=self)
    c = Card(Cards.castle("green"),240,700,batch=self)
    c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180
    for i in range(2,7,1):
      for i2 in range(5):
        if i <= 3:
          Card(Cards.yellow(),i2*120,i*100,batch=self)
        if i == 4:
          Card(Cards.gray(),i2*120,i*100,batch=self)
        if i >= 5:
          c = Card(Cards.green(),i2*120,i*100,batch=self)
          c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180

  def add(self,*args,**kwargs):
    return super().add(*args,**kwargs)

  def swap(self):
    for card in self.cards:
      card.position = (width-card.position[0]-card.w,
                       height+100-card.position[1]-card.h)
      card.image.anchor_x = 120-card.image.anchor_x
      card.image.anchor_y = 100-card.image.anchor_y
      card.rotation = 180-card.rotation

  def get_card(self,pos):
    for card in self.cards:
      if card.in_area(pos):
        return card

  def get_adjacent(self,pos):
    adjacent = []
    x,y = pos
    for card in self.cards:
      if card.in_area((x+card.w,y),(x,y+card.h),
                        (x-card.w,y),(x,y-card.h)):
        adjacent.append(card)
    return adjacent

  def update(self,x,y):
    for group in self.card_groups:
      if group.in_area((x,y)):
        return    
    for card in self.cards:
      card.update((x,y))

class Window(pyglet.window.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.batch = CardBatch()
    img = pyglet.image.load("card_one.png")
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    #self.card1 = Card(img,Cards.noone,100,110,batch=self.batch)
    #self.card2 = Card(img,Cards.speer,100,10,batch=self.batch)
    self.cal_time = 0
    pyglet.clock.schedule(self.update)
    #pyglet.clock.schedule_interval(self.print_cal_time,1)

  def update(self,dt):
    pass

  def print_cal_time(self,dt):
    print("cal_time:%s sprites:%s" % (self.cal_time,len(self.batch.cards)))

  def on_mouse_press(self,x,y,button,MOD):
    if button == mouse.LEFT:
      self.batch.update(x,y)
      sprite_above = self.batch.get_card((x,y+SPRITE_HEIGHT))
      if sprite_above != None:
        sprite_above.position = (sprite_above.position[0]+10,
                                 sprite_above.position[1])

  def on_key_press(self,KEY,MOD):
    if KEY == key.A:
      img = pyglet.image.load("card_one.png")
      for i in range(100):
        card = Card(img,0,i*10,batch=self.batch)

    if KEY == key.S:
      reference = time.time()
      self.batch.swap()
      self.cal_time = time.time()-reference
    
  def on_draw(self):
    self.clear()
    self.batch.draw()
    fps_display.draw()

if __name__ == "__main__":
  width = 600;height =800
  window = Window(width,height,"New Stucture Testing",resizable=True)
  glClearColor(255,255,255,255)
  fps_display = pyglet.window.FPSDisplay(window)
  fps_display.label.font_size = 15
  pyglet.app.run()
