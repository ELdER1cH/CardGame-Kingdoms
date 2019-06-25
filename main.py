try:
  import pyglet
  import threading
  import json
  from pyglet.gl import *
  import pop_up, Batch, Cards, Card
  from pyglet.window import key, mouse
  import chat_dependencies.main_chat as main_chat
  import random
  import client
  import screens
  
except ImportError as err:
  print("couldn't load modue. %s" % (err))

IP = 'localhost'
PORT = 8765

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
INDENTATION_RIGHT = 2

class Window(main_chat.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.batch = Batch.CardBatch()
    self.pop_up = pop_up.Pop_Up()

    self.pre_resize_dims = (self.width,self.height)
    self.scale_x = 1
    self.scale_y = 1

    self.current_screen = screens.StartScreen(self.width,self.height)
    self.ingame = False
    self.my_move = False
    
    pyglet.clock.schedule(self.update)

    self.press = [0,0,0]

  def on_close(self):
    super().on_close()
    print('programm closed!')
    try:
      self.client.s.close()
    except:
      pass

  def start_game(self,delay=0,my_move=True):
    self.ingame = True
    self.batch = Batch.CardBatch()
    self.my_move = my_move
    self.hand = self.current_screen.hand
    self.batch.castle.load_hand(self.batch.castle.y-100,False,hand=self.hand)
#send actions via client when playing
#set player who received 2. ready to waiting and the other to playing/ start
#execute actions from receive messages

  def back(self,delay):
    self.current_screen = screens.StartScreen(self.width,self.height)

  def back_l(self,delay=None):
    self.ingame = False
    self.current_screen = screens.LobbyScreen(self.width,self.height)

  def replace(self,delay,target,cardname,activate):
    target.replace(target,cardname,activate=activate,rotate=True)

  def swap(self,delay,clicked_card,target):
    clicked_card.swap(target,target.position)

  def attack(self,delay,clicked_card,target):
    won = clicked_card.fight(target,self.pop_up)
    if won:
      self.back_l()
      self.g_print("You lost!")
    
  def receive_messages(self):
      while True:
        try:
          re = self.client.s.recv(4096)
          print(re)
          r = json.loads(re.decode())
          #print("<< received %s" % r)
          if type(r) == dict:
            if r['type'] == 'lobby':
              self.client.lobby = int(r['lobby'])
              self.client.lobbysize = int(r['lobbysize'])
              self.current_screen.ready = False
              self.current_screen.opponent_ready = False
              self.client.send_lobby()
              print(f"<< lobby update: {self.client.lobby} (size: {self.client.lobbysize})")
              if self.client.lobbysize != 2 and self.ingame:
                pyglet.clock.schedule_once(self.back_l,0.01)
            elif r['type'] == 'ready':
              try:
                self.current_screen.opponent_ready = not self.current_screen.opponent_ready
                self.current_screen.ready = r['ready']
                print("mr: %s or: %s" %
                      (self.current_screen.ready, self.current_screen.opponent_ready))
                if self.current_screen.ready and self.current_screen.opponent_ready:
                  pyglet.clock.schedule_once(self.start_game,0.01)
              except:
                print("<< r['ready'] received a message for an action that could not be executed!")

            elif r['type'] == 'move_done':
              self.my_move = True
              pyglet.clock.schedule_once(self.batch.card_specials,0.01)
              print("<< your turn!")

            elif r['type'] == 'replace':
              pos, cardname = r['replace']
              pos = (480-int(pos[0]),800-int(pos[1]))
              target = self.batch.get_card(pos)
              pyglet.clock.schedule_once(self.replace,0.01,target,cardname,True)

            elif r['type'] == 'swap':
              pos1,pos2 = r['swap']
              pos1 = (480-int(pos1[0]),800-int(pos1[1]))
              pos2 = (480-int(pos2[0]),800-int(pos2[1]))
              
              clicked_card = self.batch.get_card(pos1)
              target = self.batch.get_card(pos2)
              
              pyglet.clock.schedule_once(self.swap,0.01,clicked_card,target)

            elif r['type'] == 'attack':
              pos1,pos2 = r['attack']
              pos1 = (480-int(pos1[0]),800-int(pos1[1]))
              pos2 = (480-int(pos2[0]),800-int(pos2[1]))
              
              clicked_card = self.batch.get_card(pos1)
              target = self.batch.get_card(pos2)
              
              pyglet.clock.schedule_once(self.attack,0.01,clicked_card,target)

        except Exception as err:
          print(err)
          print("Error whilst fetching server messages!")
          pyglet.clock.schedule_once(self.back,0.01)
          break

  def update(self,dt):
    self.pop_up.update(dt)
  
  def select(self,target,clicked_card):
    if target.special_tag != "immovable" or target.y == 0:
      if target.owner == self.batch.castle.owner:
        self.batch.select_card(target)
      else:
        self.pop_up.new_red_frame(target.position)
    else:
      self.pop_up.new_red_frame(target.position)

  def on_mouse_press(self,x,y,button,MOD,antir=True):
    if not self.ingame:
      cs = self.current_screen
      for b in cs.buttons:
        action = b.press(x,y,button)
        if action != None:
          if action == "ONLINE":
            self.current_screen = screens.LobbyScreen(self.width,self.height)
            try:
              self.client = client.Client(IP,PORT)
            except Exception as err:
              print(err)
              print("<> connection could not be established!")
              self.current_screen = screens.StartScreen(self.width,self.height)
              return
            threading.Thread(target=self.receive_messages).start()
            
          elif action == "BACK":
            #back to startscreen
            self.current_screen = screens.StartScreen(self.width,self.height)
          elif action == "OFFLINE":
            #load old version of game?
            print('not featured yet')
          elif action == "SETTINGS":
            #settings - later: to change server addr. (and maybe sound or sth.)
            self.current_screen = screens.SettingsScreen(self.width,self.height)
          elif action == "QUIT":
            #button of startscreen
            self.close()
          elif action == "READY":
            if self.client.lobbysize == 2:
              cs.ready = not cs.ready
              print(f"ready: {cs.ready}")
              self.client.send_ready(self.current_screen.opponent_ready)
              if self.current_screen.ready and self.current_screen.opponent_ready:
                self.start_game(my_move=False)
                self.batch.castle.mana = 2
      return
    if not self.my_move:
      return
    
    x /= self.scale_x
    y /= self.scale_y
    ###LEFT
    if button == mouse.LEFT:
      
      ###NEW CLICK/ TARGET
      target = self.batch.get_card((x,y))
      if target == None: return
      ###OLD CLICK/ SELECT
      clicked_card = self.batch.get_card(self.batch.select_frame.position)
      #MAKE SURE THERES A CARD AT THE OLD CLICK - IF THERES NONE, TARGET = NEW SELECT
      if clicked_card != None:
        ###HIDE IF DOUBLE CLICK
        if target == clicked_card:
          self.batch.hide(self.batch.select_frame)
          
        #---HAND---
        ###IF SELECT IN HAND  
        elif clicked_card.y == 0:
          ###IF TARGET NOT IN HAND
          if target.y > 0:
            ###IF TARGET IS MINE
            if target.owner == clicked_card.owner:
              ###IF TARGET IS EMPTY FIELD
              if target.special_tag == "unoccupied_field":
                #IF PLAYER HAS ENOUGH MONEY
                if self.batch.castle.mana >= clicked_card.price:
                  self.batch.castle.mana -= clicked_card.price
                  #EMPTY FIELD AND CARD IN HAND SWAP POSITIONS
                  #HAND BEFORE: - if first card were to be placed
                  #C C C C C -> after: E C C C C
                  clicked_card.swap(target,target.position,activate=True)
                  self.client.send_replace_event(clicked_card.position,clicked_card.name)
                  #in Hand: (E=empty field,C=Card in Hand) - (if first card was placed)
                  #E C C C C-> C E C C C-> C C E C C-> C C C E C-> C C C C E-> C C C C C
                  self.batch.update_hand(target)
                  self.batch.hide(self.batch.select_frame)
                  #UPDATE STATS DISPLAY TO SHOW RIGHT MANA AMOUT
                  self.batch.update_disp(clicked_card)
                else:
                  self.pop_up.new_pop_up((x,y),0.5,'TOO COSTLY: %s' % (clicked_card.price))
                  self.pop_up.new_red_frame(clicked_card.position)
              else:
                ###IF NEW CLICK NOT A EMPTY FIELD (AND MY CARD), SELECT THAT CARD
                self.select(target,clicked_card)
            else:
              ###IF TARGET IS NOT MY CARD SHOW A RED FRAME
              self.pop_up.new_red_frame(clicked_card.position)
          else:
            ###IF CARD IS IN HAND SELECT THAT CARD INSTEAD
            self.batch.select_card(target)

        #---NOT HAND---
        else:
          #GET UP, DOWN, LEFT, RIGHT TO SELECT
          adjacent = self.batch.get_adjacent(clicked_card.position)
          for in_reach in adjacent:
            ###IF NEW CARD/ TARGET IS IN REACH OF SELECT
            if target == in_reach:
              ###IF CARD IN REACH IS MY CARD
              if clicked_card.owner == target.owner:
                ##IF CARD IS NOT IMMOVABLE
                if target.special_tag != "immovable":
                  #SWAP POSITION WITH THAT CARD IN REACH
                  clicked_card.swap(target,target.position)
                  self.client.send_swap_event(clicked_card.position,target.position)
                  #MAKE SURE THE STATS DISPLAY STILL DISPLAYS THE RIGHT CARD - THEY SWAPPED, STATS WOULD DISPLAY YELLOW
                  self.batch.update_disp(clicked_card)
                else:
                  #IF CARD IN REACH == IMMOVABLE, SHOW RED FRAME
                  self.pop_up.new_red_frame(clicked_card.position)
              else:
                #IF CARD IN RANGE IS NOT MY CARD
                if self.batch.castle.mana >= 2:
                  self.batch.castle.mana -= 2
                  won = clicked_card.fight(target,self.pop_up)
                  self.client.send_attack_event(clicked_card.position,target.position)
                  if won:
                    self.back_l()
                    self.g_print("You won!")
                else:
                  self.pop_up.new_red_frame(target.position)
              ##IF TARGET WAS IN REACH, HIDE SELECT, SINCE THERE WAS A SWAO or FIGHT
              self.batch.hide(self.batch.select_frame)
              break
          else:
            ###IF CARD NOT IN REACH, TRY SELECTING THAT CARD
            self.select(target,clicked_card)

      ##SINCE THERES NO SELECTED CARD, TARGET = NEW SELECT
      elif target.special_tag != "unoccupied_field":
        #IF TARGET IS NO EMPTY FIELD, SHOW ITS STATS IN STATS DISPLAY
        ##ONLY DO THIS IF TARGET IS NOT IN ENEMY HAND
        if target.y > 0 and target.y < 800:
          self.batch.disp.update_to_enemy(target)
        #TRY SELECTING THAT CARD
        self.select(target,clicked_card)
      else:
        #IF TARGET IS EMPTY FIELD SHOW RED FRAME
        self.pop_up.new_red_frame(target.position)    


  def on_key_press(self,KEY,MOD):
    #key.ENTER & key.ESCAPE in while command_input_state; T = open chat
    super().on_key_press(KEY,MOD)
    if not self.chat_model.command_input_widget_state:
      if KEY == key.S:
        #self.batch.swap()
        if self.my_move:
          self.client.send_move_done()
          self.my_move = False
          self.batch.hide(self.batch.select_frame)
          self.batch.disp.clear()
          
      elif KEY == key.D:
        target = self.batch.get_card(self.batch.select_frame.position)
        if target != None and target.y == 0:     
          self.batch.update_hand(target)
          
  def on_draw(self):
    self.clear()
    if self.ingame:
      self.batch.draw()
      self.pop_up.draw()
    else:
      self.current_screen.draw()
    fps_display.draw()
    self.chat_model.draw()

  def on_resize(self,width,height):
    glScalef(1/self.scale_x,1/self.scale_y,1)
    self.scale_x = width/self.pre_resize_dims[0]
    self.scale_y = height/self.pre_resize_dims[1]
    #glScalef(self.scale_x,self.scale_y,1)
    glScalef(self.scale_x,self.scale_y,1)
    super().on_resize(width,height)

  def on_cmd(self,cmd):
        if cmd[0] == '/hello world':
            self.g_print('§cHello, dear fella!')
        elif cmd[0] == '/mana_cheat':
            if len(cmd) == 2:
                if cmd[1] == "-me":
                    self.batch.castle.mana = 99999
                else:
                    try:
                        self.batch.castle.mana += int(cmd[1])
                    except ValueError as err:
                        self.g_print("§cplease enter an integer as an argument! %s" % (err))
            else: self.g_print("/mana_cheat <value/-me>")
        elif cmd[0] == '/heal_cheat':
            if len(cmd) >= 2 and cmd[1] == "-me":
              self.batch.castle.health = 99999
            elif len(cmd) == 4:
              try:
                card = self.batch.get_card((int(cmd[1])*120,int(cmd[2])*100))
              except ValueError as err:
                self.g_print("§cplease enter an integer as an argument! %s" % (err))
              if card != None:
                card.health += int(cmd[3])
              else: self.g_print("no card at that coordiante")
            else: self.g_print("/heal_cheat <x-Koordiante> <y-Koordiante> <healamount>")
        elif cmd[0] == "/replace":
          if len(cmd) >= 2 and cmd[1] == "-hand":
            if cmd[2] in list(Cards.cards.keys()):
              row = self.batch.get_row((0,0))
              for card in row:
                card.replace(card,cmd[2],owner=card.owner)
            else:
              self.g_print("§cunknown card: %s" % (cmd[2]))
          else:
            self.g_print("§c/replace -hand <card_name>")

        else: self.g_print("§cunknown command. '%s'" % (" ".join(cmd)))

if __name__ == "__main__":
  width = 600+120*INDENTATION_RIGHT;height =800
  window = Window(width,height,"Cardgame - Online Version (developer build)",resizable=True,vsync=False)
  glClearColor(135,206,250,255)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  fps_display = pyglet.window.FPSDisplay(window)
  fps_display.label.font_size = 15
  pyglet.app.run()