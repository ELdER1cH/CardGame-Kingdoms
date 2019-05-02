#name,batch,level=1,health=1,attack=1,price=0,
#                 manareg=True,crit_chance=0.01,block_chance=0.01,
#                 img='resc/card_one.png',x=0,y=0
import card

def farm_special(self,c=None):#mana_reg,maxmana
    self.current_player.max_mana += 5
    self.current_player.mana_reg += 2

def healer_special(self,c=None):
    self.round_based_specials.append(self.map[self.select[0]][self.select[1]].heal)

def booster_special(self,c=None):
    i2 = int(c.sprite.x/120); i = int(c.sprite.y/100)
    
    for row in range(5):
        if self.map[i][row] != None and self.map[i][row] != 0 and self.map[i][row] != 1 and self.map[i][row] != "g":
            self.map[i][row].attack *= 2          

    


    

def bb_special(self,c=None):
    self.round_based_specials.append(self.map[self.select[0]][self.select[1]].wakeup)



cards = [ #name      level,h,dmg,cost,mana,crit,,img
    ['Schwertkämpfer',1,500,500,300,7,True,0.01,'resc/card_one.png',None,''],
    ['Turm',1,5000,5000,0,13,True,0,'resc/card_two.png',None,'immovable'],                   #unbewglich
    ['Palatin',1,2500,2500,100,12,True,0.02,'resc/palatin.png',None,''],
    ['Bauernhof',1,1500,1500,0,17,False,0,'resc/farm.png',farm_special,'immovable'],         #unbeweglich
    ['Speerkämpfer',1,400,400,350,4,True,0.05,'resc/speer.png',None,''],
    ['Healer',1,700,700,100,10,True,0,'resc/healer.png',healer_special,''],                   #special executed on swap()
    ['Orc',1,1000,800,500,9,True,0.05,'resc/Orc.png',None,''],
    ['Goblin',1,200,200,350,3,True,0,'resc/Goblin.png',None,''],
    ['Fahnenträger',1,750,750,100,22,False,0,'resc/flag.png',booster_special,''],
    ['BigBoss',1,500,10000,400,16,True,0,'resc/Godzilla.png',bb_special,'immovable'],
    ['Bombe',1,1,1,1000,11,True,0,'resc/Bomb.png',None,'wantstodie']

]


#schmerz (karten machen weniger schaden mit weniger leben) -  bestimmte karten erhöhen schmerz des gegners
#schmerz als 1 von 2 globalen specials die am anfang vom fight ausgewählt werden können