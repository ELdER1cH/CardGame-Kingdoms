from Card import Card
import Cards,random


class Castle(Card):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.mana = 0
    self.max_mana = 20
    
  def load_hand(self,y,hand=[0]):
    #Setting up Cards in Hand
    self.cards = []
    all_cards = list(Cards.cards.keys())
    placed = []
    for i in hand:
      self.cards.append(all_cards[i])
    for i in range(5):
      name = random.choice(self.cards)
      info = Cards.cards[name]
      while info[4] > 20 or name in placed:
        name = random.choice(self.cards)
        info = Cards.cards[name]
      placed.append(name)
      c = Card(name,i*120,y,batch=self.batch,owner=self.owner)
  def load_hand_offline (self,y,bo):
    for i in range(5):
      name, info = Cards.get_random()
      while info[4] > 20:
        name, info = Cards.get_random()
      c = Card(name,i*120,y,batch=self.batch,owner=self.owner)
      if bo:
        c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180