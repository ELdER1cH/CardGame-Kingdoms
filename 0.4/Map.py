import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import card, pop_up, stats_display
from random import randint

class Map:
    def __init__(self,cards,batch,opponent_batch,opponent,current_player):
        self.select = None
        self.pop_up = pop_up.Pop_Up()
        self.disp = stats_display.Stats_Display()
        self.opponent = opponent
        self.opponent_batch = opponent_batch
        self.current_player = current_player
        self.cards = cards
        self.batch=batch
        self.round_based_specials = []
        self.select_frame = pyglet.sprite.Sprite(pyglet.image.load('resc/frame.png')
                                                 ,-120,0)
        #----------------------------------------------------------------------------------------------
        self.map = [
            [None,None,None,None,None],
            [1,1,None,1,1],
            [None,None,None,None,None],
            [None,None,None,None,None],
            ["noone","noone","noone","noone","noone"],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [1,1,0,1,1]
            ]
        #----------------------------------------------------------------------------------------------
    
    def card_new_round_action(self):
        # Round specials
        for action in self.round_based_specials:
            action(self)

    def card_place_action(self):
        self.current_player.mana += -self.map[self.select[0]][self.select[1]].price
        if self.map[self.select[0]][self.select[1]].mana_reg: self.current_player.mana_reg += -1
        if self.map[self.select[0]][self.select[1]].special != None:
            self.map[self.select[0]][self.select[1]].special(self,self.map[self.select[0]][self.select[1]])

    def update(self,dt):
        self.pop_up.update(dt)
        self.disp.update(self.current_player.mana,self.current_player.max_mana,self.current_player.mana_reg,self.map,self.select)
    
    def draw(self):
        self.select_frame.draw()
        self.pop_up.draw()
        self.disp.draw()

    def update_hand(self,pos):
        if pos != 4:
            for i in range(pos+1,5,1):
                self.map[0][i].sprite.set_position((i-1)*120,0)
                self.map[0][i-1] = self.map[0][i]
                self.map[0][i] = None
        c = self.cards[randint(0,len(self.cards)-1)]
        self.map[0][4] = card.Card(c[0],self.batch,c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],x=4*120,y=0)

    def area_select(self,x,y):#,x1,y1
        #Wo wird geklickt
        #i = x in Map (Liste)
        #i2 = y in Map (Liste)
        #x1 = x in Fenster (Pixel)
        #y1 = y in Fenster (Pixel) 
        for i in range(len(self.map)):
            for i2 in range(len(self.map[i])):
                x1 = i2*120; y1 = i*100
                #Testen ob dort gklickt werden darf bzw ob es augewähtl werden darf
                if self.map[i][i2] != None and self.map[i][i2]!= 0 and self.map[i][i2]!= 1 and self.map[i][i2] != 'g' and self.map[i][i2] != 'noone':                
                    #Testen wo geklickt wird
                    if x >= x1 and x <= x1+120 and y >= y1 and y <= y1+100:
                        #Unterscheidung Hand oder Map und übergeben von variablen
                        if i < 1:
                            #              x y   Genauer
                            self.select = [i,i2,"Hand"]
                        else:
                            self.select = [i,i2,"map"]
                        #Placing Frame
                        self.select_frame.set_position(x1,y1)
                        break
                        
                
    def inside_m(self,x,y):#,x1,y1
        #Aktions mit ausgewählter Karte 
        #i = x in Map (Liste)
        #i2 = y in Map (Liste)
        #x1 = x in Fenster (Pixel)
        #y1 = y in Fenster (Pixel)
        if self.select != None:
            ##Aktionen mit Karten in der Hand
            if self.select[2] == "Hand":
                #Testen wo ist der Klick
                for i in range(1,len(self.map),1):
                    for i2 in range(len(self.map[i])):
                        #Klick Koordinaten
                        x1 = i2*120; y1 = i*100
                        #Neuer Klick abfrage
                        if self.map[i][i2] == None:                
                            if x >= x1 and x <= x1+120 and y >= y1 and y <= y1+100:
                                #Test -> Genug Mana für Karte
                                if self.current_player.mana >= self.map[self.select[0]][self.select[1]].price:
                                    self.map[self.select[0]][self.select[1]].opponent_sprite.batch = self.opponent_batch
                                    self.map[self.select[0]][self.select[1]].sprite.set_position(x1,y1)
                                    self.map[i][i2] = self.map[self.select[0]][self.select[1]]
                                    self.card_place_action()
                                    self.map[self.select[0]][self.select[1]] = None
                                    #opponent map update
                                    self.map[i][i2].opponent_sprite.set_position(600-x1,900-y1)
                                    self.opponent.map.map[8-i][4-i2] = 'g'
                                    #-------------------
                                    self.update_hand(self.select[1])
                                    self.select = None
                                    self.select_frame.set_position(-120,0)
                                    break
                                else: 
                                    self.pop_up.new_red_frame(self.select[1]*120,self.select[0]*100)
                                    break
            #Aktions mit Karten in Map
            else:
                xs,ys = self.select[0:2]
                if self.map[xs][ys].moveable != 'immovable':
                    lis = []
                    if xs > 1 and self.map[xs-1][ys] != 1:
                        lis.append([xs-1,ys])
                    if xs < 7 and self.map[xs+1][ys] != 1:
                        lis.append([xs+1,ys])
                    if ys > 0:
                        lis.append([xs,ys-1])
                    if ys < 4:
                        lis.append([xs,ys+1])
                    for m1,m2 in lis:
                        x1 =m2*120; y1 = m1*100
                        if x >= x1 and x <= x1+120 and y >= y1 and y <= y1+100:
                            if self.map[m1][m2] == None:
                                self.map[xs][ys].sprite.set_position(x1,y1)
                                self.map[m1][m2] = self.map[xs][ys]
                                #opponent map update
                                self.map[m1][m2].opponent_sprite.set_position(600-x1,900-y1)
                                self.opponent.map.map[8-m1][4-m2] = 'g'
                                self.opponent.map.map[8-xs][4-ys] = 0
                                self.map[xs][ys] = None
                                #-------------------
                                self.select = None
                                self.select_frame.set_position(-120,0)
                            elif self.current_player.mana >= 4:
                                attack_cost = 4
                                capure_cost = 5
                                if self.map[m1][m2] == 'g':
                                    opponent_card = self.opponent.map.map[8-m1][4-m2]
                                    me = self.map[xs][ys]
                                    opponent_card.health += -me.attack
                                    me.health += -opponent_card.attack/2
                                    if randint(1,100) <= me.crit_chance*100: 
                                        opponent_card.health += -me.attack*0.5
                                        self.pop_up.new_pop_up(x,y,text='%s CRIT - %s left' % (me.attack*1.5,opponent_card.health))
                                    else:
                                        self.pop_up.new_pop_up(x,y,text='%s DMG - %s left' % (me.attack,opponent_card.health))
                                    if opponent_card.health <= 0:
                                        if opponent_card.mana_reg: self.current_player.mana_reg += 1
                                        del opponent_card.sprite
                                        del opponent_card.opponent_sprite
                                        self.opponent.map.map[8-m1][4-m2] = 0
                                        self.map[m1][m2]= None
                                                                                
                                    if me.moveable == 'wantstodie' or me.health <= 0:
                                        if me.mana_reg: self.current_player.mana_reg += 1
                                        del me.sprite
                                        del me.opponent_sprite
                                        self.opponent.map.map[8-xs][4-ys] = 0
                                        self.map[xs][ys]= None
                                    self.select = None
                                    self.select_frame.set_position(-120,0)

                                    self.current_player.mana -= attack_cost
                            elif self.current_player.mana >= 5:
                                if self.map[m1][m2] == 0 or self.map[m1][m2] == 'noone':
                                    if self.map[m1][m2] == 0:
                                        self.opponent.mana_reg += -1
                                    self.map[xs][ys].sprite.set_position(x1,y1)
                                    self.map[m1][m2] = self.map[xs][ys]
                                    #opponent map update
                                    self.map[m1][m2].opponent_sprite.set_position(600-x1,900-y1)
                                    self.opponent.map.map[8-m1][4-m2] = 'g'
                                    self.opponent.map.map[8-xs][4-ys] = 0
                                    self.map[xs][ys] = None
                                    #-------------------
                                    self.select = None
                                    self.select_frame.set_position(-120,0)
                                    self.current_player.mana_reg += 1
                                    self.current_player.mana -= capure_cost
                                
                            else: break
                else: 
                    self.pop_up.new_red_frame(self.select[1]*120,self.select[0]*100)
                    
#n,n,n,n,n
#1,1,n,1,1
#n,n,n,n,n
#n,n,n,n,n
#0,0,0,0,0
#0,0,0,0,0
#0,0,0,0,0
#1,1,0,1,1       
