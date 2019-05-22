import pyglet
from Card import Card
import random
#speical_tags to yet account for: Bombe, Rammbock, (+Burg) 

cards = {
            #name level,h,   Maxh,dmg,cost,crit,img,       specials,special_tag,place_special  
            'Schwertkaempfer': [1,500,500,300,7,0.01,'resc/card_one.png',[],'',[]],
            'Turm': [1,5000,5000,0,13,0,'resc/card_two.png',[],'immovable',[]],
            'Palatin': [1,2500,2500,200,13,0.02,'resc/palatin.png',[],'',[]],
            'Bauernhof': [1,1500,1500,0,17,0,'resc/farm.png',[Card.generate_mana,Card.generate_mana,Card.generate_mana],'immovable',[Card.farm_special]],
            'Speerkaempfer': [1,400,400,350,4,0.05,'resc/speer.png',[],'',[]],
            'Healer': [1,700,700,100,10,0,'resc/healer.png',[Card.heal],'',[]],
            'Orc': [1,700,800,500,9,0.05,'resc/Orc.png',[],'',[]],
            'Goblin': [1,200,200,350,3,0,'resc/Goblin.png',[],'',[]],
            'Fahnentraeger': [1,750,750,100,22,0,'resc/flag.png',[],'',[Card.attack_booster_special]],
            'BigBoss': [1,500,10000,400,16,0,'resc/Godzilla.png',[Card.wake_up],'immovable',[]],
            'Bombe': [1,1,1,1000,3,0,'resc/Bomb.png',[],'wantstodie',[]],
            'Shield': [1,1000,1000,200,22,0,'resc/shield.png',[],'',[Card.shield_booster_special]],
            'Rammbock': [1,1500,1000,400,6,0,'resc/Rammbock.png',[],'BW',[]]
}

def get_random_name():
    #name, info = random.choice(list(Cards.cards.items()))
    return random.choice(list(cards.keys()))

def Burg(card):
    card.img = 'resc/Castle.png'
    card.level = 1
    card.name = "Burg"
    card.specials = [Card.castle_special]
    card.place_special = []
    card.health = 10000
    card.max_health = 10000
    card.dmg = 400
    card.price = 0
    card.crit = 0
    card.special_tag = "immovable"
    return pyglet.image.load(card.img)

def green(card):
    card.img = 'resc/green_frame.png'
    card.level = 1
    card.name = "green"
    card.specials = [Card.generate_mana]
    card.place_special = []
    card.health = 1
    card.max_health = 1
    card.dmg = 0
    card.price = 0
    card.crit = 0
    card.special_tag = "unoccupied_field"
    return pyglet.image.load(card.img)

def yellow(card):
    card.img = 'resc/yellow_frame.png'
    card.level = 1
    card.name = "yellow"
    card.specials = [Card.generate_mana]
    card.place_special = []
    card.health = 1
    card.max_health = 1
    card.dmg = 0
    card.crit = 0
    card.price = 0
    card.special_tag = "unoccupied_field"
    return pyglet.image.load(card.img)
    
def gray(card):
    card.img = 'resc/gray_frame.png'
    card.level = 1
    card.name = "gray_frame"
    card.specials = []
    card.place_special = []
    card.health = 1
    card.max_health = 1
    card.dmg = 0
    card.crit = 0
    card.price = 0
    card.special_tag = "unoccupied_field"
    return pyglet.image.load(card.img)

def init(card,name):
    if name == gray or name == yellow or name == green or name == Burg:
        img = name(card)
        return img
    s = cards[name]
    card.level = s[0]
    card.name = name
    card.health = s[1]
    card.max_health = s[2]
    card.dmg = s[3]
    card.price = s[4]
    card.crit = s[5]
    card.img = s[6]
    card.specials = s[7]
    card.special_tag = s[8]
    card.place_special = s[9]
    return pyglet.image.load(card.img)
