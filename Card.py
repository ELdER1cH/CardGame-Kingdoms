import pyglet
from pyglet.gl import *
import Cards
import random

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
INDENTATION = 0
INDENTATION_RIGHT = 2

class Card(pyglet.sprite.Sprite):
  def __init__(self,card_type,*args,batch,owner=None,**kwargs):
    batch.cards.append(self)
    super().__init__(Cards.init(self,card_type),*args,batch=batch,**kwargs)
    self.owner = owner
    self.init()
    
  def init(self):
    self.resize()
    self.set_dot()
    self.defend = self.dmg/2
  
  def remove(self):
    for special in self.place_special:
      special(self,-1)
    self.delete()
  
  def replace(self,target,arg,owner=True,activate=False,rotate=False):
    #anc_x,anc_y,rot = self.get_anchor()
    if owner != True: self.owner = owner
    self.image = Cards.init(target,arg)
    self.init()
    if rotate:
      self.image.anchor_x = 120; self.image.anchor_y = 100; self.rotation = 180
    else:
      self.image.anchor_x = 0
      self.image.anchor_y = 0
      self.rotation = 0
    if activate:
      for special in self.place_special:
        special(self,1)
  
  def fight(self,target,pop_up):
    won = False
    dmg = self.dmg
    defend = target.defend
    if target.special_tag == "BW":
      dmg *=1.5
      defend = 0
    if self.special_tag == "BW":
      dmg *=0.5
      defend *= 2
      if target.name == "Burg":
        dmg *= 4
        defend *=.5

    if target.special_tag == "unoccupied_field":
      #so there is no high -dmg in pop_up xD
      target.health = dmg
      
    target.health -= dmg
    self.health -= defend
    pop_up.new_pop_up(target.position,text='%s DMG - %s left'
                      % (self.dmg,target.health),life_span=0.7)
    
    if target.special_tag != "unoccupied_field":
      self.batch.update_disp(target)
                                         
    if target.health <= 0:
      if target.special_tag != "unoccupied_field":
        self.batch.update_disp(self)
      if target.name == "Burg":
        #pop_up.new_pop_up((target.position[0]+30,target.position[1]+30),text='Congrats! You won!!',life_span=5)
        won = True
        self.batch.cards = []
      if self.owner == "green":
        target.replace(target,"green",owner="green")
      else:
        target.replace(target,"yellow",owner="yellow")

    if self.health <= 0:
      if self.owner == "yellow":
        self.replace(self,"green",owner="green")
      else:
        self.replace(self,"yellow",owner="yellow")
    return won
  
  def swap(self,card,pos,activate=False):
    card.position = self.position
    self.position = pos
    if activate:
      for special in self.place_special:
        special(self,1)

  def heal(self):
    heal_amount = 1200
    cards_to_heal = 0
    adjacent = self.batch.get_adjacent(self.position)
    for card in adjacent:
      if card.owner == self.owner and card.special_tag != "unoccupied_field":
        cards_to_heal += 1
    for card in adjacent:
      if card.owner == self.owner and card.special_tag != "unoccupied_field":
        if card.health < card.max_health:
          card.health += heal_amount/cards_to_heal
          if card.health > card.max_health:
            card.health = card.max_health
          print('Healed %s at %s:%s to %s health' % (card.name,card.x/120,card.y/100,card.health))

  def wake_up(self):
    #For Sleeping Giant
    if self.health >= 5000:
      self.special_tag = ""
    else: self.special_tag = "immovable"
    
  def draw_card_special(self):
      if self.owner == self.batch.castle.owner:
          target = None
          
          for i in range(5):
              card = self.batch.get_card((SPRITE_WIDTH*i,0))
              if card.special_tag == "unoccupied_field":
                  target = card
                  break
              
          if target != None:
              target.replace(target,random.choice(self.batch.castle.cards))
              
  def generate_mana(self):
    if self.owner == self.batch.castle.owner:
      if self.batch.castle.mana < self.batch.castle.max_mana:
        self.batch.castle.mana += 1

  def farm_special(self,on_off):
    if self.batch.castle.owner == self.owner:
      self.batch.castle.max_mana += 5*on_off

  def castle_special(self):
    if self.health < self.max_health:
      self.health += 200
      if self.health > self.max_health: self.health = self.max_health

  def attack_booster_special(self,on_off):
    #Variablen
    if on_off == 1:
      mulitplier = 0.3
      self.row = self.batch.get_row(self.position)
    #Boostvorgang
    for card in self.row:
      if card.owner == self.owner:
        card.dmg += card.dmg*mulitplier*on_off

  def shield_booster_special(self,on_off):
        
    #Variablen
    if on_off == 1:
      mulitplier = 0.3
      self.row = self.batch.get_row(self.position)
    #Boostvorgang
    for card in self.row:
      if card.owner == self.owner:
        card.health += card.health*mulitplier*on_off
  
  def splash_mana(self):
    if self.owner == self.batch.castle.owner:
      if self.batch.castle.mana < self.batch.castle.max_mana:
        self.batch.castle.mana += 1

  def resize(self):
    self.image.get_texture().width = SPRITE_WIDTH
    self.image.get_texture().height = SPRITE_HEIGHT
    self.w = SPRITE_WIDTH
    self.h = SPRITE_HEIGHT

  def set_dot(self):
    base = self.image.texture
    if self.owner == "green" or self.owner == "yellow":
      texture = pyglet.image.Texture.create(width=self.w,height=self.h)
      img = pyglet.image.load("resc/"+self.owner+"_dot.png").get_image_data()
      base.blit_into(img, x=0, y=0, z=0)
   
  def in_area(self,*pos):
    mx, my = self.position
    for x,y in pos:
      if x >= mx and x < mx+self.w and y >= my and y < my+self.h:
        return True

  def update(self,pos):
    pass

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
