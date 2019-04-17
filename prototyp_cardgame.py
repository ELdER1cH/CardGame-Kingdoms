import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import card
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#rounds -player bezogen arbeiten xD
#einnehmen von feldern/ feldarten - aqua/violett/grau(unbesetzt)
#kampfsystem
#automatisch nachfüllen + mehr Karten + goldener Stapel

#stats/ anzeigen - leben, stats truppen z.b. von letztem select
#-hover funktion

#evtl. 2./ 2.0 prototyp
#besseres mapping
#inventar schrumpfen
#mehrere Karten pro Feld

class Map:
    def __init__(self):
        self.select = None
        self.select_frame = pyglet.sprite.Sprite(pyglet.image.load('resc/frame.png')
                                                 ,-120,0)

        self.map = [
            [None,None,None,None,None],
            [1,1,None,1,1],
            [None,None,None,None,None],
            [None,None,None,None,None],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [1,1,0,1,1]
            ]
        
    def update(self):
        pass
    
    def draw(self):
        self.select_frame.draw()

    def area_select(self,x,y):#,x1,y1
        for i in range(len(self.map)):
            for i2 in range(len(self.map[i])):
                x1 = i2*120; y1 = i*100
                if self.map[i][i2] != None and self.map[i][i2]!= 0 and self.map[i][i2]!= 1:                
                    if x >= x1 and x <= x1+120 and y >= y1 and y <= y1+100:
                        if i < 1:
                            self.select = [i,i2,"Hand"]
                        else:
                            self.select = [i,i2,"Map"]
                        self.select_frame.set_position(x1,y1)
                        
                
    def inside_m(self,x,y):#,x1,y1
        if self.select[2] == "Hand":
            for i in range(1,len(self.map),1):
                for i2 in range(len(self.map[i])):
                    x1 = i2*120; y1 = i*100
                    if self.map[i][i2] == None:                
                        if x >= x1 and x <= x1+120 and y >= y1 and y <= y1+100:
                            self.map[self.select[0]][self.select[1]].sprite.set_position(x1,y1)
                            self.map[i][i2] = self.map[self.select[0]][self.select[1]]
                            self.map[self.select[0]][self.select[1]] = None
                            self.select = None
                            self.select_frame.set_position(-120,0)
        else:
            xs,ys = self.select[0:2]
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
                        self.map[xs][ys] = None
                        self.select = None
                        self.select_frame.set_position(-120,0)
#n,n,n,n,n
#1,1,n,1,1
#n,n,n,n,n
#n,n,n,n,n
#0,0,0,0,0
#0,0,0,0,0
#0,0,0,0,0
#1,1,0,1,1       

class Player:
    def __init__(self):
        self.map = Map()

class Window(pyglet.window.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=False,vsync=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        #self.cardd = card.Card('Reinhard',x=0,y=0)
        #self.cardd2 = card.Card('Blümchen',img='resc/card_two.png',x=120,y=0)
        self.player1 = Player()
        self.player2 = Player()
        self.cardd = card.Card('Reinhard',x=0,y=0)
        self.cardd2 = card.Card('Blümchen',img='resc/card_two.png',x=120,y=0)
        self.player1.map.map[0][0] = self.cardd
        self.player1.map.map[0][1] = self.cardd2
        #print(cardd.cards[0].name)

        self.batch = pyglet.graphics.Batch()
        self.back = pyglet.image.load('resc/blank.png')

    def update(self,dt):
        pass

    def on_mouse_press(self,x,y,button,MOD):
        desx,desy=0,0
        dx2,dy2=0,200
        if button == mouse.LEFT:
            if self.player1.map.select == None:
                self.player1.map.area_select(x,y)
            else: self.player1.map.inside_m(x,y)
        elif button == mouse.RIGHT:
            pass

    def on_key_press(self,KEY,MOD):
        #if KEY == key.R:
        pass
        
    def on_key_release(self,KEY,MOD):
        pass

    def on_draw(self):
        self.clear()
        self.back.blit(0,100)
        self.batch.draw()
        self.cardd.sprite.draw()
        self.cardd2.sprite.draw()
        self.player1.map.draw()
    
    #def on_resize(self,w,h):
        #print(str(h))

#
        
if __name__ == "__main__":
    window = Window(600,900,'Prototyp')
    glClearColor(0.9,0.9,1,1)
    pyglet.app.run()

