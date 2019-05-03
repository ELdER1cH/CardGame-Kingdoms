import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Map ,card,player, cards
from random import randint


class Player:
    def __init__(self):
        self.cards = cards.cards
        self.mana = 0
        self.max_mana = 20
        self.mana_reg = 10
        #self.opponent = player.Player(batch)
        #self.map = map.map(self.cards,batch,self.opponent.map)
        #self.load_hand(batch)
        
    def load_hand(self,batch):
        for i in range(5):
            #['Schwertkämpfer',1,500,500,300,7,True,0.01,'resc/card_one.png',None,'']
            c = self.cards[randint(0,len(self.cards)-1)]
            self.map.map[0][i] = card.Card(c[0],batch,c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],x=i*120,y=0)
            #if c[8] != None:
            #    c[8]()
            #self.opponent.map.map[0][i] = card.Card('scheiegal',opponent_batch,img=self.cards[randint(0,1)],x=480-i*120,y=700)