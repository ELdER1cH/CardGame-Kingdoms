import pyglet

def Burg(card):
    img = pyglet.image.load('resc/Castle.png')
    card.level = 1
    card.name = "castle"
    card.mana_reg = 0
    card.specials = []
    card.place_special = None
    card.health = 10000
    card.max_health = 10000
    card.attack_dmg = 0
    card.defend_dmg = 400
    card.crit = 0
    card.mana = 0
    card.max_mana = 20
    card.price = 0
    card.special_tag = "immovable"
    return img

def Schwertkämpfer(card):
    img = pyglet.image.load('resc/card_one.png')
    card.level = 1
    card.name = "Schwertkämpfer"
    card.mana_reg = 0
    card.specials = []
    card.place_special = None
    card.health = 500
    card.max_health = 500
    card.attack_dmg = 300
    card.defend_dmg = 150
    card.price = 7
    card.crit = 0.01    
    card.special_tag = ""
    return img

def Turm(card):
    img = pyglet.image.load('resc/card_two.png')
    card.level = 1
    card.name = "Turm"
    card.mana_reg = 0
    card.specials = []
    card.place_special = None
    card.health = 5000
    card.max_health = 5000
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.price = 13
    card.crit = 0   
    card.special_tag = "immovable"
    return img

def Palatin(card):
    img = pyglet.image.load('resc/palatin.png')
    card.level = 1
    card.name = "Palatin"
    card.mana_reg = 0
    card.specials = []
    card.place_special = None
    card.health = 2500
    card.max_health = 2500
    card.attack_dmg = 200
    card.defend_dmg = 100
    card.price = 13
    card.crit = 0.02   
    card.special_tag = ""
    return img

def Bauernhof(card):
    img = pyglet.image.load('resc/farm.png')
    card.level = 1
    card.name = "Bauernhof"
    card.mana_reg = 3
    card.specials = []
    card.place_special = farm_special()
    card.health = 1500
    card.max_health = 1500
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.price = 17
    card.crit = 0   
    card.special_tag = "immovable"
    return img

def green(card):
    img = pyglet.image.load('resc/green_frame.png')
    card.level = 1
    card.name = "green_frame"
    card.mana_reg = 1
    card.specials = []#card.heal etc.
    card.place_special = None #card.some_place_special
    card.health = 1
    card.max_health = 1
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.price = 0
    card.crit = 0
    card.special_tag = "immovable"
    return img

def yellow(card):
    img = pyglet.image.load('resc/yellow_frame.png')
    card.level = 1
    card.name = "yellow_frame"
    card.mana_reg = 1
    card.specials = []
    card.place_special = None
    card.health = 1
    card.max_health = 1
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.crit = 0
    card.price = 0
    card.special_tag = "immovable"
    return img
    
def gray(card):
    img = pyglet.image.load('resc/gray_frame.png')
    card.level = 1
    card.name = "gray_frame"
    card.mana_reg = 0
    card.specials = []
    card.place_special = None
    card.health = 1
    card.max_health = 1
    card.attack_dmg = 0
    card.defend_dmg = 0
    card.crit = 0
    card.price = 0
    card.special_tag = "immovable"
    return img

cards = [Schwertkämpfer,Turm,Palatin,Bauernhof]
