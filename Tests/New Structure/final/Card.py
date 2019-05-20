import pyglet
from pyglet.gl import *

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
INDENTATION = 0
INDENTATION_RIGHT = 2

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
      img = pyglet.image.load("resc/yellow_dot.png").get_image_data()
      base.blit_into(img, x=0, y=0, z=0)
    elif self.owner == "green":
      img = pyglet.image.load("resc/green_dot.png").get_image_data()
      base.blit_into(img, x=0, y=0, z=0)
  
  def in_area(self,*pos):
    mx, my = self.position
    for x,y in pos:
      if x >= mx and x < mx+self.w and y >= my and y < my+self.h:
        return True

  def update(self,pos):
    pass

  def fight(self,oppponent):
    opponent.health -= self.attack_dmg

  def defend(self,attacker):
    attacker.health -= self.defend_dmg   

  def heal(self):
    to_heal = self.batch.get_adjacent(self.position)
    for card in to_heal:
      card.health += 100

  def farm_special(self,on_off):
    if self.batch.castle.owner == self.owner:
      self.batch.castle.max_mana += 5*on_off


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
