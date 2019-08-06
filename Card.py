import pyglet
from pyglet.gl import *
import Cards,pop_up
import random

val = 1
SPRITE_WIDTH = int(135/val)
SPRITE_HEIGHT = int(135/val)
INDENTATION = 0
INDENTATION_RIGHT = 2

left_gap = 1920//2 - 2*135

class Card(pyglet.sprite.Sprite):
  def __init__(self,card_type,*args,batch,owner=None,**kwargs):
    batch.cards.append(self)
    super().__init__(Cards.init(self,card_type),*args,batch=batch,**kwargs)
    self.owner = owner
    self.init()
    self.batch = batch
    
    
  def init(self):
    self.resize()
    self.set_dot()
    self.defend = self.dmg/2
  
  def remove(self):
    for special in self.place_special:
      special(self,-1)
    #self.delete()
  
  def replace(self,target,arg,owner=True,activate=False,rotate=False):
    #anc_x,anc_y,rot = self.get_anchor()
    if owner != True: self.owner = owner
    if activate:
      for special in self.place_special:
        special(self,1)
    self.image = Cards.init(target,arg)
    self.init()
    if rotate:
      self.image.anchor_x = 135; self.image.anchor_y = 135; self.rotation = 180
    else:
      self.image.anchor_x = 0
      self.image.anchor_y = 0
      self.rotation = 0

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
      if target.special_tag == "immovable":
        dmg *= 4
        defend *=.5

    if target.special_tag == "unoccupied_field":
      #so there is no high -dmg in pop_up xD
      target.health = dmg
      
    target.health -= dmg
    self.health -= defend

    if target.name == "Burg":
      self.batch.disp.burg_label.text = str(target.health)

    self.batch.pop_up.damage_event(pos=target.position,amount=dmg)
    
    
    if target.special_tag != "unoccupied_field":
      self.batch.update_disp(target)
                                         
    if target.health <= 0:
      if target.special_tag != "unoccupied_field":
        self.batch.update_disp(self)
      if target.name == "Burg":
        #pop_up.new_pop_up((target.position[0]+30,target.position[1]+30),text='Congrats! You won!!',life_span=5)
        won = True
        self.batch.cards = []
      target.remove()
      target.replace(target,self.owner,owner=self.owner)

    if self.health <= 0:
      #Wenn Mauer angeriffen wird
      if target.name != 'Wall':
        #feld wird mit gegnerischem Feld ersetzt
        self.remove()
        self.replace(self,target.owner,owner=target.owner)
      else:
        #feld wird mit mienem Feld ersetzt
        self.remove()
        self.replace(self,self.owner,owner=self.owner)
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
      if card.owner == self.owner and card.special_tag != "unoccupied_field" and card.health < card.max_health:
        cards_to_heal += 1
    real_heal = heal_amount/cards_to_heal
    for card in adjacent:
      if card.owner == self.owner and card.special_tag != "unoccupied_field":
        if card.health < card.max_health:
          card.health += real_heal
          if card.health > card.max_health:
            card.health = card.max_health
            real_heal = real_heal - (card.health-card.max_health)
          self.batch.pop_up.heal_special(card.position,amount=real_heal)
          print('Healed %s at %s:%s to %s health' % (card.name,card.x/135,card.y/135,card.health))

  def wake_up(self):
    #For Sleeping Giant
    if self.health >= 3000:
      self.special_tag = ""
   
  def draw_card_special(self,on_off=True):
      if on_off:
        if self.batch.online == True:
          if self.owner == self.batch.castle.owner:
              target = None
              for i in range(5):
                  card = self.batch.get_card((left_gap+SPRITE_WIDTH*(i),0))
                  if card.special_tag == "unoccupied_field":
                      target = card
                      break
                  
              if target != None:
                  target.replace(target,random.choice(self.batch.castle.cards))
        self.batch.pop_up.carddraw_event(pos=self.position)
              
  def generate_mana(self):
    if self.owner == self.batch.castle.owner:
      if self.batch.castle.mana < self.batch.castle.max_mana:
        self.batch.castle.mana += 1
        
  def farm_special(self,on_off):
      if self.owner == self.batch.castle.owner:
        self.batch.castle.max_mana += 5*on_off
      else:
        castle = self.batch.get_card((left_gap+270,954))
        castle.max_mana += 5*on_off
        if castle.mana >= castle.max_mana:
              castle.mana = castle.max_mana

  def castle_special(self):
    if self.health < self.max_health:
      self.health += 200
      if self.health > self.max_health: self.health = self.max_health

  def wall_special(self):
    self.health -= 3000
    if self.health <= 0:
        self.replace(self,"gray")
        
  def attack_booster_special(self,on_off):
    #Variablen
    multiplier = 0.5
    if on_off == 1:
      self.row = self.batch.get_row(self.position)
    #Boostvorgang
    for card in self.row:
      if card.owner == self.owner:
        if on_off == 1:
          card.dmg += card.dmg*multiplier*on_off
        else:
          card.dmg = card.dmg/(1+multiplier)

  def shield_booster_special(self,on_off):
        
    #Variablen
    multiplier = 0.5
    if on_off == 1:
      self.row = self.batch.get_row(self.position)
    #Boostvorgang
    for card in self.row:
      if card.owner == self.owner:
        if on_off == 1:
          card.health += card.health*multiplier*on_off
        else:
          card.health = card.health/(1+multiplier)

  def splash_heal(self,delay=None,target=None,dmg=None):
    heal_amount = 500 # Muss auch noch in main: splash event und Cards: Describtion geändert werden !
    if target.owner == self.owner:
        if target.health < target.max_health:
          target.health += heal_amount
        if target.health > target.max_health:
          target.health = target.max_health
          heal_amount = heal_amount - (target.health-target.max_health)
        self.batch.pop_up.heal_special(pos=target.position,amount= heal_amount)
    return False
  
  def splash_mana(self,delay=None,target=None,dmg=None):
    if self.owner == self.batch.castle.owner:
      if self.batch.castle.mana < self.batch.castle.max_mana:
        self.batch.castle.mana += 1
        self.batch.update_disp(self)
    return False
    
  def splash_damage(self,delay=None,target=None,dmg=None):
    won = False
    defend = target.defend
 

    if target.special_tag == "unoccupied_field":
      #so there is no high -dmg in pop_up xD
      target.health = dmg      
    target.health -= dmg

    if target.name == "Burg":
      self.batch.disp.burg_label.text = str(target.health)

    if target.special_tag != "unoccupied_field":
      self.batch.update_disp(target)
                                         
    if target.health <= 0:
      if target.special_tag != "unoccupied_field":
        self.batch.update_disp(self)
      if target.name == "Burg":
        #pop_up.new_pop_up((target.position[0]+30,target.position[1]+30),text='Congrats! You won!!',life_span=5)
        won = True
        self.batch.cards = []
      target.remove()

      target.replace(target,target.owner,owner=target.owner)

    return won
  
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
    self.h = 135
    self.w = 135
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
