import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import  Map , player, card, pop_up

class Game(pyglet.window.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=False,vsync=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
 
        #----------------------------------------------------------------------------------------------
        #Variablen
        self.batch = pyglet.graphics.Batch() 
        self.opponent_batch = pyglet.graphics.Batch()
        self.current_player = player.Player() #  currentplayer
        self.current_player.opponent = player.Player()
        self.current_player.map = Map.Map(self.current_player.cards,self.batch,self.opponent_batch,self.current_player.opponent,self.current_player)
        self.current_player.load_hand(self.batch)
        self.current_player.opponent.map = Map.Map(self.current_player.cards,self.opponent_batch,self.batch,self.current_player,self.current_player.opponent)
        self.current_player.opponent.load_hand(self.opponent_batch)
        self.current_player.opponent.opponent = self.current_player
        self.back = pyglet.image.load('resc/blank.png')
        self.current_player.mana += self.current_player.mana_reg
        #----------------------------------------------------------------------------------------------
        pyglet.clock.schedule(self.update)

    def swap(self):
        # Actions for swapping Players
        self.current_player = self.current_player.opponent
        self.opponent = self.current_player.opponent
        save = self.batch
        self.batch = self.opponent_batch
        self.opponent_batch = save
        #Mana Update
        self.current_player.mana += self.current_player.mana_reg
        if self.current_player.mana > self.current_player.max_mana:
            self.current_player.mana = self.current_player.max_mana
        #Calling round based actions
        self.current_player.map.card_new_round_action()
        
    def update(self,dt):
        self.current_player.map.update(dt)

    def on_mouse_press(self,x,y,button,MOD):
        if button == mouse.LEFT:
            self.current_player.map.area_select(x,y)
            self.current_player.map.inside_m(x,y)
                # self.swap()
        elif button == mouse.RIGHT:
            pass

    def on_key_press(self,KEY,MOD):
        if KEY == key.S:
            self.current_player.map.select = None
            self.current_player.map.select_frame.set_position(-120,0)
        if KEY == key.T:
            self.swap()
        
    def on_key_release(self,KEY,MOD):
        pass

    def on_draw(self):
        self.clear()
        self.back.blit(0,100)
        self.batch.draw()
        self.current_player.map.draw()
        self.current_player.map.pop_up.draw()