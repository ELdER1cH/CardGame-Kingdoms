import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Map , card

class Card:
    global_cards = []
    #specials = []
    #specials[i](mana_reg,)
    def __init__(self,name,batch,level=1,health=1,max_health=1,attack=1,price=0,
                 mana_reg=True,crit_chance=0.01,
                 img='resc/card_one.png',special=None,moveable='',x=0,y=0):
        #Variables
        self.name = name
        self.level = level
        self.health = health
        self.max_health=max_health
        self.attack = attack
        self.moveable = moveable
        self.special = special
        self.price = price
        self.mana_reg = mana_reg
        self.crit_chance = crit_chance
        self.global_cards.append(self)
        tex = pyglet.image.load(img)
        self.sprite = pyglet.sprite.Sprite(tex,x, y,batch=batch)
        self.opponent_sprite = pyglet.sprite.Sprite(tex,x, y,batch=None)   
        self.opponent_sprite.rotation = 180

    def fight(self,target):
        pass

    def wakeup(self,map):
        #For Sleeping Giant
        if self.health >= 5000:
            self.moveable = ""  
    def castle_special(self, map):
        heal_amount = 200
        castle=map.map[1][2]
        if castle.health+heal_amount <= castle.max_health:
            castle.health += heal_amount

    def heal(self,map):
        #Special for Healer
        heal_amount = 1200
        cards_to_heal = -1
        real_heal_amount= heal_amount
        try:
            i2 = int(self.sprite.x/120); i = int(self.sprite.y/100)
        except: return
        lis = []
        if i > 1 and map.map[i-1][i2] != 1:
            lis.append([i-1,i2])
        if i < 7 and map.map[i+1][i2] != 1:
            lis.append([i+1,i2])
        if i2 > 0:
            lis.append([i,i2-1])
        if i2 < 4:
            lis.append([i,i2+1])
        for m1,m2 in lis:
            if map.map[m1][m2] != None and map.map[m1][m2] != 0 and map.map[m1][m2] != 1 and map.map[m1][m2] != "g" and map.map[m1][m2] != "noone":
                cards_to_heal += 1 
        for m1,m2 in lis:
            if map.map[m1][m2] != None and map.map[m1][m2] != 0 and map.map[m1][m2] != 1 and map.map[m1][m2] != "g" and map.map[m1][m2] != "noone":
                target = map.map[m1][m2]
                real_heal_amount -= cards_to_heal*(heal_amount/4)
                if target.health+heal_amount <= target.max_health:
                    target.health+=real_heal_amount
                    print('Healed %s at %s:%s to %s health' % (target.name,m1,m2,target.health))
                else:
                    target.health+=real_heal_amount-(target.health+real_heal_amount-target.max_health)
                    print('Healed %s at %s:%s to %s health' % (target.name,m1,m2,target.health))
                
                
            
    
    def draw(self):
        self.sprite.draw()

    
        
