try:
    import pyglet
    from pyglet.gl import *
    from pyglet.window import key,mouse
    import chat_dependencies.main_chat as main_chat
    import  Map , player, card, pop_up
except ImportError as err:
  print("couldn't load modue. %s" % (err))
  
class Game(main_chat.Window):
    def __init__(self,*args):
        super().__init__(*args,resizable=True,vsync=True)
        self.g_print("§cStarting...")
        self.set_minimum_size(560, 600)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.pre_resize_dims = (self.width,self.height)
        self.scale_x = 1
        self.scale_y = 1
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
        self.current_player.map.init_castle()
        self.current_player.opponent.map.init_castle()
        #----------------------------------------------------------------------------------------------
        pyglet.clock.schedule(self.update)
        self.g_print("§cInitiation: done!")
        self.chat_model.chat.update()

    def on_cmd(self,cmd):
        if cmd[0] == '/hello world':
            self.g_print('§cHello, dear fella!')
        elif cmd[0] == '/mana_cheat':
            if len(cmd) == 2:
                if cmd[1] == "-me":
                    self.current_player.mana = 99999
                else:
                    try:
                        self.current_player.mana += int(cmd[1])
                    except ValueError as err:
                        self.g_print("§cplease enter an integer as an argument! %s" % (err))
            else: self.g_print("/mana_cheat <value/-me>")
        elif cmd[0] == '/heal_cheat':
            if len(cmd) == 4:
                if cmd[3] == "-me":
                    try:
                        self.current_player.map.map[int(cmd[2])+1][int(cmd[1])-1].health = 99999
                    except ValueError as err:
                        self.g_print("§cplease enter an integer as an choordiante! %s" % (err))

                else:
                    try:
                        self.current_player.map.map[int(cmd[2])+1][int(cmd[1])-1].health += int(cmd[3])
                    except ValueError as err:
                        self.g_print("§cplease enter an integer as an argument! %s" % (err))
        else: self.g_print("§cunknown command. '%s'" % (" ".join(cmd)))

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
        #key.ENTER & key.ESCAPE in while command_input_state; T = open chat
        super().on_key_press(KEY,MOD)
        if not self.chat_model.command_input_widget_state:
            if KEY == key.R:
                self.current_player.map.select = None
                self.current_player.map.select_frame.set_position(-120,0)
            if KEY == key.S:
                self.swap()
            if KEY == key.D:
                select = self.current_player.map.select
                if select != None:
                    if select[0] == 0:
                        del self.current_player.map.map[select[0]][select[1]].sprite
                        self.current_player.map.map[select[0]][select[1]] = None
                        self.current_player.map.update_hand(select[1])
        #if KEY == key.R:
        #    self.set_size(560,600)
        
    def on_key_release(self,KEY,MOD):
        pass

    def on_resize(self,width,height):
        glScalef(1/self.scale_x,1/self.scale_y,1)
        self.scale_x = width/self.pre_resize_dims[0]
        self.scale_y = height/self.pre_resize_dims[1]
        #glScalef(self.scale_x,self.scale_y,1)
        glScalef(self.scale_x,self.scale_y,1)
        self.current_player.map.scale_x = self.scale_x
        self.current_player.map.scale_y = self.scale_y  
        self.current_player.opponent.map.scale_x = self.scale_x
        self.current_player.opponent.map.scale_y = self.scale_y 
        super().on_resize(width,height)
        #self.pre_resize_dims = (width,height)

    def on_draw(self):
        self.clear()
        self.back.blit(0,100)
        self.batch.draw()
        self.current_player.map.draw()
        self.current_player.map.pop_up.draw()
        self.chat_model.draw()