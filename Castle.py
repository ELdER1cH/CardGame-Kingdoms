from Card import Card
import Cards,random,Window


class Castle(Card):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.mana = 0
    self.max_mana = 20
    
  def load_hand(self,y,bo,hand=[0]):
    #Setting up Cars in Hand
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
      if bo:
        c.image.anchor_x = 120; c.image.anchor_y = 100; c.rotation = 180
