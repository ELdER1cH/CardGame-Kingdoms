import pyglet
from Card import Card
import random
#speical_tags to yet account for: Bombe, Rammbock, (+Burg) 

cards = {
            #name level,h,   Maxh,dmg,cost,crit,img,       specials,special_tag,place_special  
            'Schwertkaempfer': [1,500,500,300,4,0.5,'resc\jolas\Schwertkaempfer.png',[],'',[]],
            'Turm': [1,4000,4000,0,7,0,'resc/jolas/turm.png',[Card.generate_mana],'immovable',[]],
            'Palatin': [1,3000,3000,200,12,0.02,'resc\jolas\Palatin.png',[],'',[]],
            'Bauernhof': [1,1500,1500,0,13,0,'resc/jolas/bauernhof.png',[Card.generate_mana,Card.generate_mana,Card.generate_mana],'immovable',[Card.farm_special]],
            'Speerkaempfer': [1,400,400,350,4,0.05,'resc\jolas\Speerwerfer.png',[],'',[]],
            'Healer': [1,700,700,135,10,0,'resc\jolas\Healer.png',[Card.heal],'',[]],
            'Orc': [1,700,800,500,9,0.05,'resc/jolas/ork.png',[],'',[]],
            'Goblin': [1,200,200,350,3,0,'resc\jolas\Goblin.png',[],'',[Card.draw_card_special]],
            'Fahnentraeger': [1,750,750,100,9,0,'resc\jolas\Fahnentraeger.png',[],'',[Card.attack_booster_special]],
            'BigBoss': [1,500,10000,700,16,0,'resc\jolas\Bigboss.png',[Card.wake_up],'immovable',[]],
            'Bombe': [1,1,1,1000,3,0,'resc\jolas\Bombe.png',[],'wantstodie',[]],
            'Shield': [1,1000,2000,200,9,0,'resc\jolas\Schield.png',[],'',[Card.shield_booster_special]],
            'Rammbock': [1,1500,1000,400,6,0,'resc\jolas\Rammbock.png',[],'BW',[]],
            'SplashMana': [1,0,0,0,0,0,'resc\jolas/splashmana.png',[],'splash',[Card.splash_mana,Card.splash_mana,Card.splash_mana]],
            'Dwarf': [1,1000,1000,400,8,0,'resc\jolas\Zwerg.png',[Card.draw_card_special],'',[]],
            'FireBall': [1,0,0,400,4,0,'resc\jolas/feuerball.png',[],'splash',[Card.splash_damage]],
            'Elf':  [1,600,600,500,7,0,'resc\jolas\elf.png',[Card.generate_mana],'',[]],
            'Burg': [1,5000,10000,400,0,0,'resc\jolas/burg.png',[Card.castle_special,Card.draw_card_special],"immovable",[]],
            'green': [1,1,1,0,0,0,'resc/green_frame.png',[Card.generate_mana],"unoccupied_field",[]],
            'yellow': [1,1,1,0,0,0,'resc/yellow_frame.png',[Card.generate_mana],"unoccupied_field",[]],
            'gray': [1,1,1,0,0,0,'resc/gray_frame.png',[],"unoccupied_field",[]],
            'Wall': [1,15000,15000,400,0,0,'resc/jolas/mauer.png',[Card.wall_special],"immovable",[]]
}

cards_describtion={
    'Schwertkaempfer':["""Ein einsamer Schwertkaempfer"""],
    'Turm': ["""Ein Gebäude mit viel Leben. ! Aber Achtung ! Er kann nicht verschoben werden."""],
    'Palatin': ["""Er ist mächtig und kann viel aushalten, macht aber wenig Schaden!"""],
    'Bauernhof': ["""Nütze Felder und Kornspeicher, dadurch erhöht sich dein maximales Mana um 5 und deine Manaregeneration um 2."""],
    'Speerkaempfer': ["""Vorsicht vor den Speeren, die sind spitz!"""],
    'Healer': ["""Sie heilt 1200 Leben und verteilt sie gerecht unter nahen Landsleuten."""],
    'Orc': ["""Stark und hässlich"""],
    'Goblin': ["""Dieser kleine Dieb hat eine Karten in seinem Beutel. Nütze sie!"""],
    'Fahnentraeger': ["""Die Moral ist gestärkt und alle Truppen dieser Reihe machen 1,5x Schaden"""],
    'Shield': ["""Durch diesen Panzertrupp werden die Leben aller Einheiten dieser Reihe um 1,5x verstärkt"""],
    'BigBoss': ["""Er muss bis auf 5000 Leben geheilt werden, damit er aufwacht, aber dann ist er nicht mehr aufzuhalten."""],
    'Bombe': ["""Starker, aber einmaliger Schaden ... Effektiv!"""],
    'Rammbock': ["""Diese Einheit machen gegen Gebäude 1,5x Schaden, bekommt aber von normalen Einheiten 1,5x Schaden, hat keinen Verteidigungsschaden und macht an normalen Einheiten 0,5x Schaden."""],
    'SplashMana': ["""Schnelle drei Mana ... Was gibt es besseres?"""],
    'Dwarf': ["""Zwergen sind missmutig, dieser auch! Aber befördert eine Karte pro Runde ans Tageslicht."""],
    'FireBall': ["""Achtung Heiß!"""],
    'Elf':["""Sie werden sehr alt, es sei denn sie sterben im Kampf. Doch durch ihr gewaltiges Wissen wirken sie sich nicht auf deine Mana Regeneration aus."""],
    'Burg': ["""Sie ist unter allen Umständen zu schützen! Sollte sie zerstört werden, wirst du auf das Schaffot geführt. """],
    'green': [""" """],
    'yellow': ["""42 Gramm Fett"""],
    'gray': [""" """],
    'Wall': ["""Du solltest dich bedanken, sie schützt dich vor dem Feind. Doch nur 6 Runden lang und nicht vor Feuerbällen ... und Mexikanern."""]
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
