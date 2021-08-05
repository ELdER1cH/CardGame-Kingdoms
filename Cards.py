import pyglet
from Card import Card
import random
 

cards = {
            #name level,h,   Maxh,dmg,cost,Laufweite,img,       specials,special_tag,place_special, max Stamina , Mana Reg
            'Schwertkaempfer': [1,500,500,300,4,1,'resc\jolas\Schwertkaempfer.png',[Card.RegenStamina],'',[],1,1],
            'Turm': [1,6000,6000,400,7,0,'resc/jolas/turm.png',[Card.generate_mana],'immovable',[],1,1],
            'Paladin': [1,3000,3000,200,7,1,'resc\jolas\Palatin.png',[Card.RegenStamina],'',[],1,1],
            'Bauernhof': [1,1500,1500,0,13,0,'resc/jolas/bauernhof.png',[Card.generate_mana,Card.generate_mana,Card.generate_mana],'immovable',[Card.farm_special],1,1],
            'Speerkaempfer': [1,400,400,400,4,1,'resc\jolas\Speerwerfer.png',[Card.RegenStamina],'',[],1,1],
            'Heiler': [1,700,700,135,10,1,'resc\jolas\Healer.png',[Card.heal,Card.RegenStamina],'',[],1,1],
            'Orc': [1,700,800,500,9,1,'resc/jolas/ork.png',[Card.RegenStamina],'',[],1,1],
            'Goblin': [1,200,200,350,3,1,'resc\jolas\Goblin.png',[Card.RegenStamina],'',[Card.draw_card_special],1,1],
            'Fahnentraeger': [1,750,750,100,9,1,'resc\jolas\Fahnentraeger.png',[Card.RegenStamina],'',[Card.attack_booster_special],1,1],
            'Drache': [1,500,7000,700,16,0,'resc\jolas\Bigboss.png',[Card.wake_up,Card.RegenStamina],'immovable',[],1,0.5],
            'Bombe': [1,1,1,1000,3,5,'resc\jolas\Bombe.png',[],'wantstodie',[],1,1],
            'Schild': [1,1000,2000,200,9,1,'resc\jolas\Schield.png',[Card.RegenStamina],'',[Card.shield_booster_special],1,1],
            'Rammbock': [1,1500,1000,400,6,1,'resc\jolas\Rammbock.png',[Card.RegenStamina],'BW',[],1,1],
            'Mana': [1,0,0,0,0,0,'resc\jolas/splashmana.png',[],'splash',[Card.splash_mana,Card.splash_mana,Card.splash_mana],1,1],
            'Heal': [1,0,0,0,5,0,'resc\jolas/splash_heal.png',[],'splash',[Card.splash_heal],1,1],
            'Feuerball': [1,0,0,400,4,0,'resc\jolas/feuerball.png',[],'splash',[Card.splash_damage],1,1],
            'Zwerg': [1,1000,1000,400,8,1,'resc\jolas\Zwerg.png',[Card.draw_card_special,Card.RegenStamina],'',[],1,1],    
            'Elf':  [1,600,600,500,7,1,'resc\jolas\elf.png',[Card.generate_mana,Card.RegenStamina],'',[],1,1],
            'Burg': [1,5000,10000,400,0,0,'resc\jolas/burg.png',[Card.castle_special,Card.draw_card_special],"immovable",[],0,0],
            'green': [1,1,1,0,0,0,'resc/green_frame.png',[Card.generate_mana],"unoccupied_field",[],0,0],
            'yellow': [1,1,1,0,0,0,'resc/yellow_frame.png',[Card.generate_mana],"unoccupied_field",[],0,0],
            'gray': [1,1,1,0,0,0,'resc/gray_frame.png',[],"unoccupied_field",[],0,0],
            'Wall': [1,15000,15000,400,0,0,'resc/jolas/mauer.png',[Card.wall_special],"immovable",[],0,0],
            'Empty': [1,1,1,1,0,0,'resc\empty_card.png',[],"empty",[],0,0]
}

cards_describtion={
    'Schwertkaempfer':["""Ein einsamer Schwertkaempfer"""],
    'Turm': ["""Ein Gebäude mit viel Leben. ! Aber Achtung ! Er kann nicht verschoben werden."""],
    'Paladin': ["""Er ist mächtig und kann viel aushalten, macht aber wenig Schaden!"""],
    'Bauernhof': ["""Nütze Felder und Kornspeicher, dadurch erhöht sich dein maximales Mana um 5 und deine Manaregeneration um 2."""],
    'Speerkaempfer': ["""Vorsicht vor den Speeren, die sind spitz!"""],
    'Heiler': ["""Sie heilt 1200 Leben und verteilt sie gerecht unter nahen Landsleuten."""],
    'Orc': ["""Stark und hässlich"""],
    'Goblin': ["""Dieser kleine Dieb hat eine Karte in seinem Beutel. 
(Ziehe sofort eine extra Karte) 
Nütze sie!"""],
    'Fahnentraeger': ["""Die Moral ist gestärkt und alle Truppen dieser Reihe machen 1,5x Schaden"""],
    'Schild': ["""Durch diesen Panzertrupp werden die Leben aller Einheiten dieser Reihe um 1,5x verstärkt"""],
    'Drache': ["""Er muss bis auf 3000 Leben geheilt werden, damit er aufwacht, aber dann ist er nicht mehr aufzuhalten."""],
    'Bombe': ["""Starker, aber einmaliger Schaden ... Effektiv!"""],
    'Rammbock': ["""Diese Einheit machen gegen Gebäude 1,5x Schaden, bekommt aber von normalen Einheiten 1,5x Schaden, hat keinen Verteidigungsschaden und macht an normalen Einheiten 0,5x Schaden."""],
    'Mana': ["""Schnelle drei Mana ... Was gibt es besseres?"""],
    'Heal': ["""Diese Karte heilt die Zielkarte um 500 Leben. 
Hinweis: Diese Karte kann bei allen eigenen Karten eingesetzt werden."""],
    'Feuerball': ["""Achtung Heiß!
Hinweis: Diese Karte kann überall eingesetzt werden."""],
    'Zwerg': ["""Zwergen sind missmutig, dieser auch! Aber befördert eine Karte pro Runde ans Tageslicht."""],
    'Elf':["""Sie werden sehr alt, es sei denn sie sterben im Kampf. Doch durch ihr gewaltiges Wissen wirken sie sich nicht auf deine Mana Regeneration aus."""],
    'Burg': ["""Sie ist unter allen Umständen zu schützen! Sollte sie zerstört werden, wirst du auf das Schaffot geführt. """],
    'green': [""" """],
    'yellow': ["""42 Gramm Fett"""],
    'gray': [""" """],
    'Wall': ["""Du solltest dich bedanken, sie schützt dich vor dem Feind. Doch nur 6 Runden lang und nicht vor Feuerbällen ... und Mexikanern."""],
    'Empty': ["""Gähnende Leere"""]
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
    card.img = s[6]
    card.specials = s[7]
    card.special_tag = s[8]
    card.place_special = s[9]
    card.stamina = s[5]
    card.max_stamina = s[10]
    card.stamina_reg = s[11]
    card.description = d[0]
    
    return pyglet.image.load(card.img)
