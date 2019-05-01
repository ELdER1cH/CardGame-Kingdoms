import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Window, Map , card

class Card:
    cards = []
    def __init__(self,name,batch,level=1,health=1,attack=1,price=0,
                 manareg=True,crit_chance=0.01,block_chance=0.01,
                 img='resc/card_one.png',x=0,y=0):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack
        self.price = price
        self.manareg = manareg
        self.crit_chance = crit_chance
        self.block_chance = block_chance
        self.cards.append(self)
        tex = pyglet.image.load(img)
        self.sprite = pyglet.sprite.Sprite(tex,x, y,batch=batch)
        self.opponent_sprite = pyglet.sprite.Sprite(tex,x, y,batch=None)   
        self.opponent_sprite.rotation = 180     

    def attack(self,target):
        pass
    
    def draw(self):
        self.sprite.draw()

    
        
