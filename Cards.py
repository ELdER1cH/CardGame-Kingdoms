import pyglet
from Card import Card
import random
#speical_tags to yet account for: Bombe, Rammbock, (+Burg) 

cards = {
            #name level,h,   Maxh,dmg,cost,crit,img,       specials,special_tag,place_special  
            'Schwertkaempfer': [1,500,500,300,7,0.01,'resc\jolas\Schwertkaempfer.png',[],'',[]],
            'Turm': [1,5000,5000,0,13,0,'resc/tower.png',[],'immovable',[]],
            'Palatin': [1,2500,2500,200,13,0.02,'resc\jolas\Palatin.png',[],'',[]],
            'Bauernhof': [1,1500,1500,0,17,0,'resc/farm.png',[Card.generate_mana,Card.generate_mana,Card.generate_mana],'immovable',[Card.farm_special]],
            'Speerkaempfer': [1,400,400,350,4,0.05,'resc\jolas\Speerwerfer.png',[],'',[]],
            'Healer': [1,700,700,135,10,0,'resc\jolas\Healer.png',[Card.heal],'',[]],
            'Orc': [1,700,800,500,9,0.05,'resc/Orc.png',[],'',[]],
            'Goblin': [1,200,200,350,3,0,'resc\jolas\Goblin.png',[],'',[Card.draw_card_special]],
            'Fahnentraeger': [1,750,750,100,22,0,'resc\jolas\Fahnentraeger.png',[],'',[Card.attack_booster_special]],
            'BigBoss': [1,500,10000,700,16,0,'resc\jolas\Bigboss.png',[Card.wake_up],'immovable',[]],
            'Bombe': [1,1,1,1000,3,0,'resc\jolas\Bombe.png',[],'wantstodie',[]],
            'Shield': [1,1000,1000,200,22,0,'resc\jolas\Schield.png',[],'',[Card.shield_booster_special]],
            'Rammbock': [1,1500,1000,400,6,0,'resc\jolas\Rammbock.png',[],'BW',[]],
            'SplashMana': [1,0,0,0,0,0,'resc\splash_mana.jpg',[],'splash',[Card.splash_mana,Card.splash_mana,Card.splash_mana]],
            'Dwarf': [1,1000,1000,400,9,0,'resc\jolas\Zwerg.png',[],'',[]],
            'Burg': [1,5000,10000,400,0,0,'resc/Castle.png',[Card.castle_special,Card.draw_card_special],"immovable",[]],
            'green': [1,1,1,0,0,0,'resc/green_frame.png',[Card.generate_mana],"unoccupied_field",[]],
            'yellow': [1,1,1,0,0,0,'resc/yellow_frame.png',[Card.generate_mana],"unoccupied_field",[]],
            'gray': [1,1,1,0,0,0,'resc/gray_frame.png',[],"unoccupied_field",[]],
            'Wall': [1,15000,15000,400,0,0,'resc/wall.png',[Card.wall_special],"immovable",[]]
}

cards_describtion={
    'Schwertkaempfer':["""Ein einsamer Schwertkaempfer"""],
    'Turm': ["""Ein Gebäude mit viel Hp
                Aber Achtung !
                Er kann nicht verschoben werden"""],
    'Palatin': [""" """],
    'Bauernhof': [""" """],
    'Speerkaempfer': [""" """],
    'Healer': [""" """],
    'Orc': [""" """],
    'Goblin': [""" """],
    'Fahnentraeger': [""" """],
    'BigBoss': [""" """],
    'Bombe': [""" """],
    'Shield': [""" """],
    'Rammbock': [""" """],
    'SplashMana': [""" """],
    'Dwarf': [""" """],
    'Burg': [""" """],
    'green': [""" """],
    'yellow': [""" """],
    'gray': [""" """],
    'Wall': [""" """]
}



def init(card,name):
    s = cards[name]
    d = cards_describtion[name]
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
    card.description = d[0]
    
    return pyglet.image.load(card.img)
