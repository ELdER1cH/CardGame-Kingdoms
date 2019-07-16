from Card import Card
import Cards,random

width = 1920;height =1080
left_gap = width//2 - 2*135

class Castle(Card):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.mana = 0
    self.max_mana = 20
    
  def load_hand(self,y,hand=[i for i in range(len(Cards.cards)-5)],bo=False):
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
      c = Card(name,i*135+left_gap,y,batch=self.batch,owner=self.owner)
      if bo:
          c.image.anchor_x = 135; c.image.anchor_y = 135; c.rotation = 180
  
