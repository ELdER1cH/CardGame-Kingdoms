import pyglet
from pyglet.gl import *
import Cards

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
    self.resize()
    self.set_dot()

  def fight(self,oppponent):
    opponent.health -= self.attack_dmg

  def defend(self,attacker):
    attacker.health -= self.defend_dmg   

  def heal(self):
    heal_amount = 1200
    cards_to_heal = -1
    real_heal_amount= heal_amount
    lis = self.batch.get_adjacent(self.position)
    for card in lis:
        if card.owner == self.owner:
            cards_to_heal += 1 
    for card in lis:
        if card.owner == self.owner:
            target = card
            real_heal_amount -= cards_to_heal*(heal_amount/4)
            if target.health+heal_amount <= target.max_health:
                target.health+=real_heal_amount
                print('Healed %s at %s:%s to %s health' % (target.name,target.x/120,target.y/100,target.health))
            else:
                target.health+=real_heal_amount-(target.health+real_heal_amount-target.max_health)
                print('Healed %s at %s:%s to %s health' % (target.name,target.x/120,target.y/100,target.health))

  def wake_up(self):
    #For Sleeping Giant
    if self.health >= 5000:
      self.special_tag = ""
    else: self.special_tag = "immovable"
    
  def generate_mana(self):
    if self.owner == self.batch.castle.owner:
      if self.batch.castle.mana < self.batch.castle.max_mana:
        self.batch.castle.mana += 1

  def farm_special(self,on_off):
    if self.batch.castle.owner == self.owner:
      self.batch.castle.max_mana += 5*on_off

  def castle_special(self):
    self.health += 200

  def attack_booster_special(self,on_off):
    #Variablen
    if on_off == 1:
      mulitplier = 0.3
      self.row = self.batch.get_row(self.position)
    #Boostvorgang
    for card in row:
      if card.owner == self.owner:
        card.dmg += card.dmg*mulitplier*on_off

  def shield_booster_special(self,on_off):
    #Variablen
    if on_off == 1:
      mulitplier = 0.3
      self.row = self.batch.get_row(self.position)
    #Boostvorgang
    for card in row:
      if card.owner == self.owner:
        card.health += card.health*mulitplier*on_off

  def remove(self):
    self.place_special(-1)
    self.delete()
  
  def replace(self,func,owner=True):
    if owner != True: self.owner = owner 
    self.image = func(self)
  
  def resize(self):
    self.image.get_texture().width = SPRITE_WIDTH
    self.image.get_texture().height = SPRITE_HEIGHT
    self.w = SPRITE_WIDTH
    self.h = SPRITE_HEIGHT

  def set_dot(self):
    if self.place_special != None:
      self.place_special(1)
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
