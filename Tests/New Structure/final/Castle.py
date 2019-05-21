from Card import Card

class Castle(Card):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.mana = 0
    self.max_mana = 20
    self.load_hand()
    
  def load_hand(self):
    pass
