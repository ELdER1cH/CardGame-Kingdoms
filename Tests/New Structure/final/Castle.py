from Card import Card
import Cards
import random

class Castle(Card):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.mana = 0
    self.max_mana = 20
    
  def load_hand(self,y,bo):
    #Setting up Cars in Hand
    for i in range(5):
      name, info = random.choice(list(Cards.cards.items()))
      while info[4] > 20:
        name, info = random.choice(list(Cards.cards.items()))
      c = Card(name,i*120,y,batch=self.batch,owner=self.owner)
      if bo:
        c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180
