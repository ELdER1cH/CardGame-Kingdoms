import pyglet
from pyglet.gl import *
from random import randint
import time
import pop_up
from pyglet.window import key, mouse
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
INDENTATION = 0
INDENTATION_RIGHT = 2

class Cards:
  def green(card):
    img = pyglet.image.load('green_frame.png')#green_frame
    card.name = "green_frame"
    card.specials = [card.generate_mana]#card.heal etc.
    card.place_special = None #card.some_place_special
    card.health = 1
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.special_tag = "immovable"
    return img

  def yellow(card):
    img = pyglet.image.load('yellow_frame.png')
    card.name = "yellow_frame"
    card.specials = [card.generate_mana]
    card.place_special = None
    card.health = 1
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.special_tag = "immovable"
    return img
    
  def gray(card):
    img = pyglet.image.load('gray_frame.png')
    card.name = "gray_frame"
    card.specials = []
    card.place_special = None
    card.health = 1
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.special_tag = "immovable"
    return img
    
  def castle(card):
    img = pyglet.image.load('Castle.png')
    card.name = "castle"
    card.specials = []
    card.place_special = None
    card.health = 10000
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.mana = 0
    card.special_tag = "immovable"
    return img
    
class Card(pyglet.sprite.Sprite):
  def __init__(self,card_type,*args,batch,owner=None,**kwargs):
    batch.cards.append(self)
    super().__init__(card_type(self),*args,batch=batch,**kwargs)
    
    self.owner = owner

    self.resize()

    self.set_dot()

  def replace(self,func,owner=True):
    if owner != True: self.owner = owner 
    self.image = func(self)
  
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
      if x >= mx and x < mx+self.w and y >= my and y < my+self.h:
        return True

  def fight(self,oppponent):
    opponent.health -= self.attack_dmg

  def defend(self,attacker):
    attacker.health -= self.defend_dmg   

  def heal(self):
    to_heal = self.batch.get_adjacent(self.position)
    for card in to_heal:
      card.health += 100

  def generate_mana(self):
    if self.batch.castle.owner == self.owner:
      self.batch.castle.mana += 1
    
  def update(self,pos):
    pass
    #if self.in_area((pos)):
    #  self.position = (self.position[0]+10,self.position[1])
      

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
      if x >= mx and x <= mx+self.w and y > my and y < my+self.h:
        return True      
      
class CardBatch(pyglet.graphics.Batch):      
  def __init__(self):
    super().__init__()
    self.cards = []
    self.card_groups = []
    self.init_map()
    self.select_frame = pyglet.sprite.Sprite(pyglet.image.load("frame.png"),
                                             -SPRITE_WIDTH,
                                             -SPRITE_HEIGHT)
  def select_card(self,target):
    self.select_frame.position = target.position

  def add(self,*args,**kwargs):
    return super().add(*args,**kwargs)

  def swap(self):
    self.castle = self.get_card((240+120*INDENTATION,700))
    for card in self.cards:
      card.position = (width-card.position[0]-card.w-INDENTATION_RIGHT*120,
                       height+100-card.position[1]-card.h)
      card.image.anchor_x = 120-card.image.anchor_x
      card.image.anchor_y = 100-card.image.anchor_y
      card.rotation = 180-card.rotation
      for special in card.specials:
        special()
    self.hide(self.select_frame)

  def hide(self,card):
    card.position = (-SPRITE_WIDTH,-SPRITE_HEIGHT)

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

  def update(self,pos):
    pass
    #for group in self.card_groups:
    #  if group.in_area(pos):
    #    return    
    #for card in self.cards:
    #  card.update(pos)

  def draw(self):
    super().draw()
    self.select_frame.draw()

  def init_map(self):
    self.castle = Card(Cards.castle,240+120*INDENTATION,100,batch=self,owner="yellow")
    c = Card(Cards.castle,240+120*INDENTATION,700,batch=self,owner="green")
    c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180
    for i in range(2,7,1):
      for i2 in range(0+INDENTATION,5+INDENTATION,1):
        if i <= 3:
          Card(Cards.yellow,i2*120,i*100,batch=self,owner="yellow")
        if i == 4:
          Card(Cards.gray,i2*120,i*100,batch=self,owner="gray")
        if i >= 5:
          c = Card(Cards.green,i2*120,i*100,batch=self,owner="green")
          c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180

class Window(pyglet.window.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)

    #batch functions:
    #swap | get_card(pos) | get_adjacent(pos) | (update(pos))
    #select_card(target)
    self.batch = CardBatch()
    self.pop_up = pop_up.Pop_Up()
    
    pyglet.clock.schedule(self.update)

  def update(self,dt):
    self.pop_up.update(dt)

  def on_mouse_press(self,x,y,button,MOD):
    #left click?
    if button == mouse.LEFT:
      clicked_card = self.batch.get_card((x,y))
      #clicked on a card?
      if clicked_card != None:
        select = self.batch.get_card(self.batch.select_frame.position)
        #is there already an selected card?
        if select != None:
          if clicked_card.owner == self.batch.castle.owner :
            if select != clicked_card:
              adjacent = self.batch.get_adjacent(select.position)
              for allowed_card in adjacent:
                #if clicked card adjacent to select
                if clicked_card == allowed_card:
                    #now stuff could happen - attack, move, etc.

                    #move if own field
                    p = clicked_card.position
                    clicked_card.position = select.position
                    select.position = p
                    self.batch.hide(self.batch.select_frame) 
                    return
              self.pop_up.new_red_frame(select.position)
            else:
              #undo select
              self.batch.hide(self.batch.select_frame)
              
          else:
            #indicate error with red_frame
            self.pop_up.new_red_frame(select.position)   
          
          #set select if own card and not immovable
        elif clicked_card.owner == self.batch.castle.owner:
          if clicked_card.special_tag != "immovable":
            self.batch.select_card(clicked_card)
            #target.replace(Cards.gray,owner="gray")
          else:
            self.pop_up.new_red_frame(clicked_card.position)
        else:
            self.pop_up.new_red_frame(clicked_card.position)
        
      

      #self.batch.update((x,y))
      #sprite_above = self.batch.get_card((x,y+SPRITE_HEIGHT))
      #if sprite_above != None:
      #  sprite_above.position = (sprite_above.position[0]+10,
      #                           sprite_above.position[1])

  def on_key_press(self,KEY,MOD):
    if KEY == key.A:
      img = pyglet.image.load("card_one.png")
      for i in range(100):
        Card(Cards.gray,0,i*10,batch=self.batch,owner="gray")
    elif KEY == key.S:
      self.batch.swap()
      print(self.batch.castle.mana)
      
    
  def on_draw(self):
    self.clear()
    self.batch.draw()
    self.pop_up.draw()
    fps_display.draw()

if __name__ == "__main__":
  width = 600+120*INDENTATION_RIGHT;height =800
  window = Window(width,height,"New Stucture Testing",resizable=True)
  glClearColor(255,255,255,255)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  fps_display = pyglet.window.FPSDisplay(window)
  fps_display.label.font_size = 15
  pyglet.app.run()

"""
CONTAINER:

  for time calculation:
reference = time.time()
self.cal_time = time.time()-reference

  in __init__:
self.cal_time = 0
pyglet.clock.schedule_interval(self.print_cal_time,1)

  to add:
def print_cal_time(self,dt):
  print("cal_time:%s sprites:%s" % (self.cal_time,len(self.batch.cards)))

"""
