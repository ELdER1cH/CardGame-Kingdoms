import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Window, Map ,card,player
from random import randint


class Player:
    def __init__(self):
        self.cards = ['resc/card_one.png','resc/card_two.png']
        #self.opponent = player.Player(batch)
        #self.map = Map.Map(self.cards,batch,self.opponent.map)
        #self.load_hand(batch)
        
    def load_hand(self,batch):
        for i in range(5):
            self.map.map[0][i] = card.Card('scheiegal',batch,img=self.cards[randint(0,1)],x=i*120,y=0)
            #self.opponent.map.map[0][i] = card.Card('scheiegal',opponent_batch,img=self.cards[randint(0,1)],x=480-i*120,y=700)
            