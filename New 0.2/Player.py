import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Map ,card,player, cards
from random import randint


class Player:
    def __init__(self):
        #Variables
        self.cards = cards.cards
        self.mana = 0
        self.max_mana = 20
        self.mana_reg = 10
        #self.opponent = player.Player(batch)
        #self.map = map.map(self.cards,batch,self.opponent.map)
        #self.load_hand(batch)
        
    def load_hand(self,batch):
        #Setting up Cars in Hand
        for i in range(5):
            c = self.cards[randint(0,len(self.cards)-1)]
            self.map.map[0][i] = card.Card(c[0],batch,c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],x=i*120,y=0)
            