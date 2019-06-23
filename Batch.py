import pyglet
from pyglet.gl import *
import Cards, Card, stats_display
from Castle import Castle
import random

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
INDENTATION = 0
INDENTATION_RIGHT = 2
width = 600+120*INDENTATION_RIGHT;height =800

class CardBatch(pyglet.graphics.Batch):      
  def __init__(self):
    super().__init__()
    self.cards = []
    self.card_groups = []
    self.disp = stats_display.Stats_Display()
    self.select_frame = pyglet.sprite.Sprite(pyglet.image.load("resc/frame.png"),
                                             -SPRITE_WIDTH,
                                             -SPRITE_HEIGHT)
    self.init_cards()
    self.mana_reg = 0

  def card_specials(self,delay=None):
    for card in self.cards:
      for special in card.specials:
        if card.y > 0 and card.y < 800 and card.owner == self.castle.owner:
          special(card)
    self.update_disp(self.castle)
    
  def swap(self):
    self.castle = self.get_card((240+120*INDENTATION,700))
    for card in self.cards:
      card.position = (width-card.position[0]-card.w-INDENTATION_RIGHT*120,
                       height+100-card.position[1]-card.h)
      card.image.anchor_x = 120-card.image.anchor_x
      card.image.anchor_y = 100-card.image.anchor_y
      card.rotation = 180-card.rotation
      for special in card.specials:
        if card.y > 0 and card.y < 800 and card.owner == self.castle.owner:
          special(card)
    self.hide(self.select_frame)
    self.update_disp(self.castle)

  def update_hand(self,target):
    row = []
    pos = target.position
    for i in range(int(pos[0]/120),5,1):
      for card in self.cards:
        if card.in_area((int(120*i),0)):
          row.append(card)
          
    for card in row:
      target.swap(card,card.position)
    target.replace(target,random.choice(self.castle.cards))

  def update_disp(self,target):
    self.mana_reg = 0
    for card in self.cards:
      for special in card.specials:
        if card.y > 0 and card.y < 800 and card.owner == self.castle.owner:
          if special == Card.Card.generate_mana:  
            self.mana_reg += 1
    self.disp.update(self.castle.mana,self.castle.max_mana,
                     self.mana_reg,target)
    
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
      if card.in_area((x+card.w,y),(x,y+card.h),
                        (x-card.w,y),(x,y-card.h)):
        adjacent.append(card)
    return adjacent

  def get_row(self,pos):
    row = []
    x,y = pos
    for card in self.cards:
      if card.in_area((0,y),(120,y),
                      (240,y),(360,y),(480,y)):
        row.append(card)
    return row

  def draw(self):
    super().draw()
    self.select_frame.draw()
    self.disp.draw()

  def init_cards(self):
    self.castle = Castle("Burg",240+120*INDENTATION,100,batch=self,owner="yellow")
    #self.castle.load_hand(self.castle.y-100,False)
    self.castle.mana = 10
    c = Castle("Burg",240+120*INDENTATION,700,batch=self,owner="green")
    c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180
    #c.load_hand(c.y+100,True)
    for i in range(2,7,1):
      for i2 in range(0+INDENTATION,5+INDENTATION,1):
        if i <= 3:
          Card.Card("yellow",i2*120,i*100,batch=self,owner="yellow")
        if i == 4:
          Card.Card("gray",i2*120,i*100,batch=self,owner="gray")
        if i >= 5:
          c = Card.Card("green",i2*120,i*100,batch=self,owner="green")
          c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180
    self.update_disp(self.castle)
    
  def update(self,pos):
    self.disp.mana_label.text = """
        Mana: %s
        Max Mana: %s
        Mana Reg: %s""" % (self.castle.mana,self.max_mana,self.mana_reg)
