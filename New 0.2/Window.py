import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import  Map , Player, card
class Window(pyglet.window.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=False,vsync=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        #self.cardd = card.Card('Reinhard',x=0,y=0)
        #self.cardd2 = card.Card('Blümchen',img='resc/card_two.png',x=120,y=0)
        self.player1 = Player.Player()
        self.player2 = Player.Player()
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