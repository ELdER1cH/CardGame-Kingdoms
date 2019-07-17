import pyglet
from pyglet.gl import *
import Cards, Card, stats_display, pop_up
from Castle import Castle
import random


val = 1
SPRITE_WIDTH = int(135/val)
SPRITE_HEIGHT = int(135/val)
INDENTATION = 0
INDENTATION_RIGHT = 2
width = 1920;height =1080
left_gap = width//2 - 2*135

class CardBatch(pyglet.graphics.Batch):      
  def __init__(self):
    super().__init__()
    self.cards = []
    self.card_groups = []
    self.disp = stats_display.Stats_Display()
    self.select_frame = pyglet.sprite.Sprite(pyglet.image.load("resc/frame.png"),
                                             -SPRITE_WIDTH,
                                             -SPRITE_HEIGHT)
    #Decides if game is online or offline
    self.online = True
    self.mana_reg = 0    
    self.round_counter = 1
    self.pop_up = pop_up.Pop_Up()

  def init_cards(self):
    self.castle = Castle("Burg",width//2,135,batch=self,owner="yellow")
    self.castle.mana = 10
    c = Castle("Burg",width//2,945,batch=self,owner="green")
    c.image.anchor_x = 135; c.image.anchor_y = 135; c.rotation = 180
    # only happening if game is offline
    if not self.online:
      self.castle.load_hand(self.castle.y-135,bo=False)
      c.load_hand(c.y+135,bo=True)
    for i in range(2,7,1):
      for i2 in range(0+INDENTATION,5+INDENTATION,1):
        if i <= 3:
          Card.Card("yellow",i2*135+left_gap,i*135,batch=self,owner="yellow")
        if i == 4:
          Card.Card("Wall",i2*135+left_gap,i*135,batch=self,owner="gray")
        if i >= 5:
          c = Card.Card("green",i2*135+left_gap,i*135,batch=self,owner="green")
          c.image.anchor_x = 135; c.image.anchor_y = 135; c.rotation = 180
    self.update_disp(self.castle)

  def swap(self):
    self.castle = self.get_card((width//2,945))
    for card in self.cards:
      card.position = ((135*4+left_gap)-card.position[0]+left_gap,height-card.position[1])
      card.image.anchor_x = 135-card.image.anchor_x
      card.image.anchor_y = 135-card.image.anchor_y
      card.rotation = 180-card.rotation
    for card in self.cards:  
      for special in card.specials:
        if card.y > 0 and card.y < 1080 and card.owner == self.castle.owner:
          special(card) 
          if card.special_tag == 'unoccupied_field':
            self.pop_up.mana_event(card.position)
          if card.name == 'Bauernhof':
            self.pop_up.mana_event(card.position,3)
    self.hide(self.select_frame)
    self.update_disp(self.castle)

  def card_specials(self,delay=None):
    for card in self.cards:
      for special in card.specials:
        if card.y > 0 and card.y < 1080:
          special(card)
    self.update_disp(self.castle)

  def grouped_card_specials(self,delay=None,group=False,gray=False):
    for card in self.cards:
      for special in card.specials:
        if card.y > 0 and card.y < 1080:
          if not gray:
            if group and card.owner == self.castle.owner: 
              special(card)
            elif not group and card.owner != self.castle.owner:
              special(card)
          elif card.owner != "yellow" and card.owner != "green":
            special(card)
    if group:
          self.round_counter += 1
      
    self.update_disp(self.castle)

  def update_hand(self,target):
    row = []
    pos = target.position
    for i in range(int((pos[0]-left_gap)/(135)),5,1):
      for card in self.cards:
        if card.in_area((int(135*i)+left_gap,0)):
          row.append(card)
          
    for card in row:
      target.swap(card,card.position)
    #only happening if game is offline
    if not self.online:  
      target.replace(target,random.choice(self.castle.cards))

  def update_disp(self,target):
    self.mana_reg = 0
    for card in self.cards:
      for special in card.specials:
        if card.y > 0 and card.y < 1080 and card.owner == self.castle.owner:
          if special == Card.Card.generate_mana:  
            self.mana_reg += 1
    self.disp.update(self.castle.mana,self.castle.max_mana,
                     self.mana_reg,target,self.round_counter)

  def select_card(self,target):
    self.select_frame.position = target.position
    self.update_disp(target)

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
      if card.in_area((x+card.w+2,y),(x,y+card.h+2),
                        (x-card.w+2,y),(x,y-card.h+2)):
        adjacent.append(card)
    return adjacent

  def get_row(self,pos):
    row = []
    x,y = pos
    for card in self.cards:
      if card.in_area((0,y),(135,y),
                      (135*2,y),(135*3,y),(135*4,y)):
        row.append(card)
    return row

  def draw(self):
    super().draw()
    self.select_frame.draw()
    self.pop_up.draw()
    self.disp.draw()

  def update(self,pos):

    self.disp.mana_label.text = """
        Mana: %s
        Max Mana: %s
        Mana Reg: %s""" % (self.castle.mana,self.max_mana,self.mana_reg)

