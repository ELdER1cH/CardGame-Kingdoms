try:
  import pyglet
  import time
  import threading, json, random, screens
  from pyglet.gl import *
  import pop_up, Batch, Cards, Card, client
  from pyglet.window import key, mouse
  import chat_dependencies.main_chat as main_chat

except ImportError as err:
  print("couldn't load modue. %s" % (err))

#all files: 1285 lines of code (28.06.19 22:55)
#79.231.167.136

#python -m auto_py_to_exe
IP = "game02.gameserver.gratis"#"localhost"
PORT = 29428

val = 1
SPRITE_WIDTH = int(135/val)
SPRITE_HEIGHT = int(135/val)
INDENTATION_RIGHT = 2
left_gap = 1920//2 - 2*135

class Window(main_chat.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)

    self.pop_up = pop_up.Pop_Up()
    self.pre_resize_dims = (self.width,self.height)
    self.scale_x = 1
    self.scale_y = 1
    self.IP = IP

    self.loading_text = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/loading.png"),700,400)
    self.wappen = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/wappen_small.png"),20,800)

    self.weiter_button = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/weitergeben_button.png"),left_gap+135*6,10)

    self.current_screen = screens.StartScreen(1920,1080)
    self.ingame = False
    self.my_move = False
    self.online = False #was True by default..
    self.lead_execute = False

    self.loading = True
    
    self.init_batch()

    self.on_resize(800,450)
#------------------------------ Game Stuff --------------------------------------

  def init_batch(self,delay=None):
    self.batch = Batch.CardBatch()
    #time.sleep(2)
    self.loading = False

  def start_game(self,delay=0,my_move=True):
    hand = []
    #self.batch = Batch.CardBatch()
    self.batch = Batch.CardBatch()
    # Sets online state for game 
    self.batch.online = self.online
    # Initialising Cards
    self.batch.init_cards()
    self.ingame = True
    self.my_move = my_move
    self.lead_execute = my_move
    if self.online:
      hand = self.current_screen.hand_selection.hand
      self.batch.castle.load_hand(self.batch.castle.y-135,hand=hand)
    if self.my_move:
      self.pop_up.your_turn_pop_up(0.01,(width//2,height//2))
    self.loading = False
    
  def replace(self,delay,target,cardname,activate):
    target.replace(target,cardname,activate=activate,rotate=False)

  def swap(self,delay,clicked_card,target):
    clicked_card.swap(target,target.position)

  def attack(self,delay,clicked_card,target):
    won = clicked_card.fight(target,self.pop_up)
    if won:
      self.back_l()
      self.g_print("You lost!")
  
  def update(self,dt):
    self.batch.pop_up.update(dt)
    self.pop_up.update(dt) 
    self.current_screen.update(dt) 
              
  def splash_event(self,clicked_card,target):
    if self.batch.castle.mana >= clicked_card.price:
      self.batch.castle.mana -= clicked_card.price
      if clicked_card.name == 'SplashMana':
            self.batch.pop_up.mana_event(target.position,3)
      elif clicked_card.name == 'FireBall':
            self.batch.pop_up.explosion_event(pos=target.position)
            self.batch.pop_up.damage_event(pos=target.position,amount=clicked_card.dmg)
            if self.online == True:
                self.safe_send(self.client.send_splash_attack_event(target.position,clicked_card.dmg))
      elif clicked_card.name == 'SplashHeal':
        if self.online == True:
                self.safe_send(self.client.send_splash_heal_event(target.position,500))
      won = None
      for special in clicked_card.place_special:
        won = special(clicked_card,target=target,dmg=clicked_card.dmg)
      clicked_card.replace(clicked_card,clicked_card.owner)
      self.batch.update_hand(clicked_card)
      
      
      if won:
          if self.online:
              self.back_l()
          else:
            self.ingame = False
            self.back()
          self.g_print("You won!")
      self.batch.hide(self.batch.select_frame)
#------------------------------ System / Strukture -------------------------------------------------------- 
  def select(self,target,clicked_card):
    if target.special_tag != "immovable" or target.y == 0:
      if target.owner == self.batch.castle.owner:
        self.batch.select_card(target)
      else:
        self.pop_up.new_red_frame(target.position)
    else:
      self.pop_up.new_red_frame(target.position)

  def start_client(self,delay=None):
    self.current_screen = screens.LobbyScreen(1920,1080)
    try:
      self.client = client.Client(self.IP,PORT)
    except Exception as err:
      print(err)
      self.g_print("<> connection could not be established!")
      print(f"({self.IP}:{PORT})")
      self.current_screen = screens.StartScreen(1920,1080)
      self.loading = False
      return
    threading.Thread(target=self.receive_messages).start()
    self.online = True
    self.batch.online = True
    self.loading = False
  
  def on_mouse_press(self,x,y,button,MOD,antir=True):
    if not self.ingame:
      self.button_actions(x,y,button,MOD,antir)
      return

    
    x /= self.scale_x
    y /= self.scale_y
    ###LEFT
    if button == mouse.LEFT:
        if x >= self.weiter_button.position[0]:
          if x >= self.weiter_button.position[0] and x < self.weiter_button.position[0]+self.weiter_button.width and y >= self.weiter_button.position[1] and y < self.weiter_button.position[1]+self.weiter_button.height:
                self.weitergeben()
                return
        
        ###NEW CLICK/ TARGET
        target = self.batch.get_card((x,y))
        if target == None: return
        if target.special_tag == 'empty': 
          self.pop_up.new_red_frame(target.position)
          return
        ###OLD CLICK/ SELECT
        clicked_card = self.batch.get_card(self.batch.select_frame.position)
        #Wenn ich nicht dran bin kann ich nur Karten anschauen aber nicht bewegen
        if not self.my_move:
          if target.special_tag != 'empty' and target.special_tag != 'unoccupied_field':
            self.batch.select_card(target)
          else:
            self.pop_up.new_red_frame(target.position) 
          return
        #MAKE SURE THERES A CARD AT THE OLD CLICK - IF THERES NONE, TARGET = NEW SELECT
        if clicked_card != None:
          #if clicked_card.special_tag ==  'empty':
           # self.pop_up.new_red_frame(target.position)
          #else:  
            ###HIDE IF DOUBLE CLICK
            if target == clicked_card:
              self.batch.hide(self.batch.select_frame)
            elif clicked_card.special_tag == 'empty':
              self.batch.hide(self.batch.select_frame)
            #---HAND---
            ###IF SELECT IN HAND  
            elif clicked_card.y == 0:
              ###IF TARGET NOT IN HAND
              if target.y > 0:
                # What happens wenn it's a Splash card
                if clicked_card.special_tag == "splash": self.splash_event(clicked_card,target); return     
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
                      clicked_card.swap(target,target.position)
                      if self.online:
                          self.safe_send(self.client.send_replace_event(clicked_card.position,clicked_card.name))
                      self.batch.update_hand(target)
                      self.batch.hide(self.batch.select_frame)
                      for special in clicked_card.place_special:
                        special(clicked_card,1)
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
              ###IF NEW CARD/ TARGET IS IN REACH OF SELECT e.g in reach of it
              if target in adjacent:
                ###IF CARD IN REACH IS MY CARD
                if clicked_card.owner == target.owner:
                  ##IF CARD IS NOT IMMOVABLE
                  if target.special_tag != "immovable":
                    print(clicked_card.stamina)
                    if clicked_card.stamina >= 1:
                      clicked_card.stamina -= 1
                      #SWAP POSITION WITH THAT CARD IN REACH
                      clicked_card.swap(target,target.position)
                      if self.online == True:
                        self.safe_send(self.client.send_swap_event(clicked_card.position,target.position))
                      #MAKE SURE THE STATS DISPLAY STILL DISPLAYS THE RIGHT CARD - THEY SWAPPED, STATS WOULD DISPLAY YELLOW
                      self.batch.update_disp(clicked_card)
                    else:
                      self.pop_up.new_pop_up((x,y),0.5,'NOT ENOUGH STAMINA: %s' % (clicked_card.stamina))
                      self.pop_up.new_red_frame(clicked_card.position)    
                  else:
                    #IF CARD IN REACH == IMMOVABLE, SHOW RED FRAME
                    self.pop_up.new_red_frame(clicked_card.position)
                else:
                  #IF CARD IN RANGE IS NOT MY CARD
                  if self.batch.castle.mana >= 2:
                    self.batch.castle.mana -= 2
                    won = clicked_card.fight(target,self.pop_up)
                    if self.online == True:
                      self.safe_send(self.client.send_attack_event(clicked_card.position,target.position))
                    if won:
                        if self.online:
                            self.back_l()
                        else:
                          self.ingame = False
                          self.back()
                        self.g_print("You won!")
                  else:
                    self.pop_up.new_red_frame(target.position)
                ##IF TARGET WAS IN REACH, HIDE SELECT, SINCE THERE WAS A SWAO or FIGHT
                self.batch.hide(self.batch.select_frame)
              else:
                ###IF CARD NOT IN REACH, TRY SELECTING THAT CARD
                if target.special_tag != "unoccupied_field":
                  self.select(target,clicked_card)


        ##SINCE THERES NO SELECTED CARD, TARGET = NEW SELECT
        elif target.special_tag != "unoccupied_field":
          #IF TARGET IS NO EMPTY FIELD, SHOW ITS STATS IN STATS DISPLAY
          ##ONLY DO THIS IF TARGET IS NOT IN ENEMY HAND
          if target.y > 0 and target.y < 1080:
            self.batch.disp.update_to_enemy(target)
          #TRY SELECTING THAT CARD
          self.select(target,clicked_card)
        else:
          #IF TARGET IS EMPTY FIELD SHOW RED FRAME
          self.pop_up.new_red_frame(target.position)    

  def button_actions(self,x,y,button,MOD,antir):
      cs = self.current_screen #tf, is this not in use? xD
      for b in cs.buttons:
        action = b.press((x / self.scale_x), (y / self.scale_y),button)
        if action != None:
          if action == "ONLINE":
            self.loading = True
            pyglet.clock.schedule_once(self.start_client,0.2)
          elif action == "SETTINGS":
            #settings - later: to change server addr. (and maybe sound or sth.)
            self.current_screen = screens.SettingsScreen(1920,1080,self.IP)
          elif action == "QUIT":
            #button of startscreen
            self.close()
          elif action == "CARDS":
                self.current_screen = screens.CardScreen(1920,1080)
          elif action == "READY":
            if self.client.opponent_found and len(self.current_screen.hand_selection.hand) >= 5:
              cs.ready = not cs.ready
              print(f"ready: {cs.ready}")
              self.safe_send(self.client.send_ready(self.current_screen.opponent_ready))
              self.current_screen.update_ready_button()
              if self.current_screen.ready and self.current_screen.opponent_ready:
                self.start_game(my_move=False)
                self.batch.castle.mana = 0
                self.batch.round_counter = 0
          elif action == "StartGameOffline":
            self.online = False
            self.start_game()
            self.batch.castle.mana = 10
            self.batch.round_counter = 1
          elif action == "BACK":
            self.ingame = False
            self.back()
            try:
              self.client.s.close()
            except:
              pass
          elif "NEWIP" in action:
              self.IP = action[5:]
              self.g_print(self.IP)
          elif action == "Page->":
            if self.current_screen.hand_selection.page < 2:
              self.current_screen.hand_selection.update_page(1)
          elif action == "Page<-":
            if self.current_screen.hand_selection.page > 1:
              self.current_screen.hand_selection.update_page(-1)

  def weitergeben(self):
    if self.online == True:
          #self.batch.swap()
      if self.my_move:
        self.safe_send(self.client.send_move_done())
        self.my_move = False
        self.batch.hide(self.batch.select_frame)
        self.batch.disp.clear()
        self.batch.grouped_card_specials(group=False)
        if self.lead_execute:
              self.batch.grouped_card_specials(gray=True) 
        #s:2x r: 2x                
    else:
      
      if self.batch.castle.owner == 'yellow':
            self.batch.grouped_card_specials(gray=True) 
            self.batch.round_counter += 1
      
      self.batch.swap()
    self.batch.disp.burg_label.text = str(int(self.batch.castle.health))
            
  def on_key_press(self,KEY,MOD):
    #key.ENTER & key.ESCAPE in while command_input_state; T = open chat
    super().on_key_press(KEY,MOD)
    if KEY == key.F11:
          self.set_fullscreen(not self.fullscreen)
    if not self.chat_model.command_input_widget_state:
      if self.ingame:
          if KEY == key.S:
            self.weitergeben()
              
          elif KEY == key.D:
            target = self.batch.get_card(self.batch.select_frame.position)
            if target != None:
                if target.y == 0:    
                    self.batch.update_hand(target)
                    target=None
                elif target.owner == self.batch.castle.owner and target.y > 135 and target.y < 135*7:
                        self.batch.hide(self.batch.select_frame)
                        self.batch.castle.mana += target.price-1
                        target.remove()
                        target.replace(target,target.owner)
                        if self.batch.castle.mana > self.batch.castle.max_mana:
                            self.batch.castle.mana = self.batch.castle.max_mana
                        if self.online:
                            if target.name == "yellow":
                                self.safe_send(self.client.send_replace_event(target.position,"green"))
                            else:
                                self.safe_send(self.client.send_replace_event(target.position,"yellow"))
                        self.batch.update_disp(self.batch.castle)
            
          elif KEY == key.C:
              print("close")
              try:
                  self.client.s.close()
              except:
                  pass
              self.back()
              self.ingame = False
      elif type(self.current_screen) == screens.SettingsScreen:
          self.current_screen.ip_textbox.new_key(key.symbol_string(KEY))
        
  def on_close(self):
    super().on_close()
    print('programm closed!')
    try:
      self.client.s.close()
    except:
      pass        
  
  def on_draw(self):
    self.clear()
    if not self.loading:
      if self.ingame:
        self.batch.draw()
        self.pop_up.draw()
        self.weiter_button.draw()
      else:
        self.current_screen.draw()
      fps_display.draw() 
      self.chat_model.draw()  
    else:
          self.loading_text.draw()
          self.wappen.draw()       

  def on_resize(self,width,height):
    if width >= 853 and height >= 480:
      glScalef(1/self.scale_x,1/self.scale_y,1)
      self.scale_x = width/self.pre_resize_dims[0]
      self.scale_y = height/self.pre_resize_dims[1]
      #glScalef(self.scale_x,self.scale_y,1)
      glScalef(self.scale_x,self.scale_y,1)
      super().on_resize(width,height)
    else:
          self.set_size(853,480)
          self.set_minimum_size(853, 480)

  def on_cmd(self,cmd):
    #self.server.on_cmd(cmd)
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
            card = self.batch.get_card((int(cmd[1])*135+left_gap,int(cmd[2])*135))
          except ValueError as err:
            self.g_print("§cplease enter an integer as an argument! %s" % (err))
          if card != None:
            card.health += int(cmd[3])
          else: self.g_print("no card at that coordiante")
        else: self.g_print("/heal_cheat <x-Koordiante> <y-Koordiante> <healamount>")
    elif cmd[0] == "/replace":
      if len(cmd) >= 2 and cmd[1] == "-hand":
        if cmd[2] in list(Cards.cards.keys()):
          row = self.batch.get_row((left_gap,0))
          for card in row:
            card.replace(card,cmd[2],owner=card.owner)
        else:
          self.g_print("§cunknown card: %s" % (cmd[2]))
      else:
        self.g_print("§c/replace -hand <card_name>")
    else: self.g_print("§cunknown command. '%s'" % (" ".join(cmd)))

  def on_chat(self,msg):
    if self.online:
      self.safe_send(self.client.send_chat_message(msg))
      print(f"send msg '{msg}' to opponent")
      
#------------------------ Server Stuff ------------------------------------------
  
  def back(self,delay=None):
    self.ingame = False #would adding these be wise??
    self.online = False
    self.current_screen = screens.StartScreen(1920,1080)

  def back_l(self,delay=None):
    #print("back_l")
    self.ingame = False
    self.current_screen = screens.LobbyScreen(1920,1080)

  def jjjjoin(self,delay=None):
    #print("jjjoin")
    if not self.ingame:
      self.client.opponent_found = True
      pyglet.clock.schedule_once(self.current_screen.update_opponent_search, 0.01, self.client.opponent_found)
      #print(self.client.opponent_found)

  def dt_g_print(self,delay,msg):
    self.g_print(msg)
    print(f"got '{msg}' and printed it in chat")

  def handle_message(self,r):
      if type(r) == dict:
                if r['type'] == 'abort':
                  self.current_screen.ready = False
                  self.current_screen.opponent_ready = False
                  self.client.opponent_found = False
                  if self.ingame:
                    #print("ini backL")
                    pyglet.clock.schedule_once(self.back_l,0.01)
                  if not self.ingame:
                    pyglet.clock.schedule_once(self.current_screen.update_opponent_search, 0.01, self.client.opponent_found)
                    pyglet.clock.schedule_once(self.current_screen.update_ready_button, 0.01)

                elif r["type"] == "join":
                  #print("join")
                  pyglet.clock.schedule_once(self.jjjjoin, 0.05)

                elif r['type'] == 'chat_message':
                  msg = "§g>> " + r['msg']
                  pyglet.clock.schedule_once(self.dt_g_print, 0.05, msg)

                elif r['type'] == 'lobby':
                  self.client.lobby = int(r['lobby'])
                  self.client.lobbysize = int(r['lobbysize'])
                  self.current_screen.ready = False
                  self.current_screen.opponent_ready = False
                  self.safe_send(self.client.send_lobby())
                  print(f"<< lobby update: {self.client.lobby} (size: {self.client.lobbysize})")
                  if self.client.lobbysize != 2 and self.ingame:
                    pyglet.clock.schedule_once(self.back_l,0.01)
                  if not self.ingame:
                    pyglet.clock.schedule_once(self.current_screen.update_opponent_search, 0.01, self.client.lobbysize)

                elif r['type'] == 'ready':
                  try:
                    self.current_screen.opponent_ready = not self.current_screen.opponent_ready
                    self.current_screen.ready = r['ready']
                    print("myready: %s opponentready: %s" %
                          (self.current_screen.ready, self.current_screen.opponent_ready))
                    if self.current_screen.ready and self.current_screen.opponent_ready:
                      self.loading = True
                      pyglet.clock.schedule_once(self.start_game,0.1)
                  except:
                    print("<< r['ready'] received a message for an action that could not be executed!")
    
                elif r['type'] == 'move_done':
                  self.my_move = True
                  pyglet.clock.schedule_once(self.batch.grouped_card_specials,0.01,True)
                  if not self.lead_execute:
                    pyglet.clock.schedule_once(self.batch.grouped_card_specials,0.01,gray=True)
                  #print("<< your turn!")
                  pyglet.clock.schedule_once(self.pop_up.your_turn_pop_up,0.01,(self.width//2,self.height//2))
                  
                elif r['type'] == 'replace':
                  pos, cardname = r['replace']
                  pos = ((135*4+left_gap)-int(pos[0])+left_gap,1080-int(pos[1]))
                  target = self.batch.get_card(pos)
                  pyglet.clock.schedule_once(self.replace,0.01,target,cardname,False)
    
                elif r['type'] == 'swap':
                  pos1,pos2 = r['swap']
                  pos1 = ((540+left_gap)-int(pos1[0])+left_gap,1080-int(pos1[1]))
                  pos2 = ((540+left_gap)-int(pos2[0])+left_gap,1080-int(pos2[1]))
                  print("p1:%s, p2:%s" % (pos1,pos2))
                  
                  clicked_card = self.batch.get_card(pos1)
                  target = self.batch.get_card(pos2)
                  
                  pyglet.clock.schedule_once(self.swap,0.01,clicked_card,target)
    
                elif r['type'] == 'attack':
                  pos1,pos2 = r['attack']
                  pos1 = ((540+left_gap)-int(pos1[0])+left_gap,1080-int(pos1[1]))
                  pos2 = ((540+left_gap)-int(pos2[0])+left_gap,1080-int(pos2[1]))
                  
                  clicked_card = self.batch.get_card(pos1)
                  target = self.batch.get_card(pos2)
                  
                  pyglet.clock.schedule_once(self.attack,0.01,clicked_card,target)

                elif r['type'] == 'splash_attack':
                  pos1,dmg = r['attack']
                  pos1 = ((540+left_gap)-int(pos1[0])+left_gap,1080-int(pos1[1]))
                  target = self.batch.get_card(pos1)
                  if dmg > 0:
                    pyglet.clock.schedule_once(self.batch.pop_up.explosion_event,0.01,pos=target.position)
                    pyglet.clock.schedule_once(self.batch.pop_up.damage_event,0.01,pos=target.position,amount=dmg)
                  pyglet.clock.schedule_once(target.splash_damage,0.01,target,dmg)
                
                elif r['type'] == 'splash_heal':
                  pos1,heal_amount = r['target']
                  pos1 = ((540+left_gap)-int(pos1[0])+left_gap,1080-int(pos1[1]))
                  target = self.batch.get_card(pos1)
                  pyglet.clock.schedule_once(self.batch.pop_up.heal_special,0.01,pos=target.position,amount=heal_amount)
                  pyglet.clock.schedule_once(target.splash_heal,0.01,target,heal_amount)

  def safe_send(self,message):
    try:
      self.client.send(message)
    except Exception as err:
      print(f"\n{err}\n")
      self.client.s.close()
      print("Verbindung zu Server beendet!")
      self.ingame = False
      self.back()

  def receiver(self,socket,bits=1096):
    buffer = ""
    while True:
      try:
        data = socket.recv(bits).decode()
        if not data: break #reading a zero length string (?) after connection is dropped ^^
        buffer += data
      except Exception as err:
        print(f"\n{err}\n")
        break
      if "\n" in buffer:
        (message, buffer) = buffer.split("\n", 1)
        yield message
    socket.close()
    print("Verbindung zu Server beendet!")
    pyglet.clock.schedule_once(self.back,0.01)
    
  def receive_messages(self):
    recv = self.receiver(self.client.s)
    for message in recv:
      print(f"- received: {message}")
      data = json.loads(message)
      self.handle_message(data)        
        
if __name__ == "__main__":
  width = 1920;height = 1080
  window = Window(width,height,"Cardgame - Online Version (developer build)",resizable=True,vsync=True)
  #window.maximize()
  #window.set_fullscreen(True)
  icon1 = pyglet.image.load('resc/16x16.png')
  icon2 = pyglet.image.load('resc/32x32.png')
  window.set_icon(icon1, icon2)
  glClearColor(135,206,250,255)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  fps_display = pyglet.window.FPSDisplay(window)
  fps_display.label.font_size = 15
  pyglet.app.run()
