import pyglet
from pyglet.gl import *
import Cards, Card, Castle

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
    self.init_map()
    self.select_frame = pyglet.sprite.Sprite(pyglet.image.load("resc/frame.png"),
                                             -SPRITE_WIDTH,
                                             -SPRITE_HEIGHT)
  def select_card(self,target):
    self.select_frame.position = target.position

  def swap(self):
    self.castle = self.get_card((240+120*INDENTATION,700))
    for card in self.cards:
      card.position = (width-card.position[0]-card.w-INDENTATION_RIGHT*120,
                       height+100-card.position[1]-card.h)
      card.image.anchor_x = 120-card.image.anchor_x
      card.image.anchor_y = 100-card.image.anchor_y
      card.rotation = 180-card.rotation
      for special in card.specials:
        special(card)
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

  def init_map(self):
    self.castle = Castle.Castle(Cards.Burg,240+120*INDENTATION,100,batch=self,owner="yellow")
    c = Castle.Castle(Cards.Burg,240+120*INDENTATION,700,batch=self,owner="green")
    c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180
    for i in range(2,7,1):
      for i2 in range(0+INDENTATION,5+INDENTATION,1):
        if i <= 3:
          Card.Card(Cards.yellow,i2*120,i*100,batch=self,owner="yellow")
        if i == 4:
          Card.Card(Cards.gray,i2*120,i*100,batch=self,owner="gray")
        if i >= 5:
          c = Card.Card(Cards.green,i2*120,i*100,batch=self,owner="green")
          c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180

  def update(self,pos):
    pass
