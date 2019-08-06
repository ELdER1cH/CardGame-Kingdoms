import pyglet
from pyglet.window import mouse, key
from main import Window
import Cards
from pyglet.gl import *

val = 1
SPRITE_WIDTH = int(135/val)
SPRITE_HEIGHT = int(135/val)
INDENTATION = 0
INDENTATION_RIGHT = 2

class Button(pyglet.sprite.Sprite):
  def __init__(self,img,*args,adj_anchor=True,**kwargs):
    if adj_anchor:
      img.anchor_x = img.width//2
      img.anchor_y = img.height//2
    super().__init__(img,*args,**kwargs)
    self.action = None

  def press(self,x,y,button):
    if button == mouse.LEFT:
      xp,yp = self.position
      xp -= self.image.anchor_x; yp -= self.image.anchor_y
      if x >= xp and x < xp+self.width and y >= yp and y < yp+self.height:
        return self.action
    return None

class TextBox(pyglet.sprite.Sprite):
  def __init__(self,img,*args,adj_anchor=False,**kwargs):
    if adj_anchor:
      img.anchor_x = img.width//2
      img.anchor_y = img.height//2
    super().__init__(img,*args,**kwargs)
    self.action = None
    self.active = False
    self.label = pyglet.text.Label('',
                                              font_name ='Arial',
                                              font_size=25,
                                              bold=False,
                                              x=self.position[0]+55, y=self.position[1]+61,
                                              color=(0,0,0,255))
    self.text = ""
    self.is_blink = False

  def press(self,x,y,button):
    if button == mouse.LEFT:
      xp,yp = self.position
      xp -= self.image.anchor_x; yp -= self.image.anchor_y
      if x >= xp and x < xp+self.width and y >= yp and y < yp+self.height:
        self.active = not self.active
        if self.active:
            self.image = pyglet.image.load("resc/active_ip_settings.png")
            self.label.text = self.text
        else:
            self.image = pyglet.image.load("resc/unactive_ip_settings.png")
            return "NEWIP" + self.text
    return None

  def blink(self):
      self.is_blink = not self.is_blink
      
      if self.is_blink:
          self.label.text = self.text + "|"
      else:
          self.label.text = self.text

  def new_key(self,KEY):
      if len(self.text) > 0:
          if KEY == "BACKSPACE":
              self.text = self.text[:-1]
              self.label.text = self.text 
      if len(self.text) < 15:
          if KEY == "_0" or KEY == "_1" or KEY == "_2" or KEY == "_3" or KEY == "_4" or KEY == "_5" or KEY == "_6" or KEY == "_7" or KEY == "_8" or KEY == "_9" or KEY == "PERIOD":
              if KEY != "PERIOD":
                  self.text += KEY[1:]
              else: self.text += "."
              
          self.label.text = self.text      

class HandSelection:
    def __init__(self,batch,width,height):
        self.hand = []#[0,1,2,3,4,5,6,7,8,9,10,11,12]#
        self.max_hand_lenght = 10
        """
        mesh:
        x,x,x,x,x    | all_cards
        x,x,x,x,x    |
        x,x,x,x,x    |
        .........    | selected
        """
        self.h = height
        self.w = width
        self.batch = batch
        self.all_card_indentation = 100
        self.frame_height_gain = 120
        self.gap = 20
        self.cpr = 8
        self.page = 1
        
        self.action = None
        self.height = 3*(135+self.gap)+self.gap   
        self.width = self.cpr*(135+self.gap)+(135+self.gap)*2
        self.position = (30,(height-self.height-450))        
        
        self.background = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/card_selection_frame.png"),self.position[0],self.position[1]+135+self.gap*2)

        self.grass_row = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/grass_row.png"),self.position[0],self.position[1])
        # Sprites in Pool
        self.page_label = pyglet.text.Label("",
                            font_name='Times New Roman', font_size=40,
                            color=(0, 0, 0,255),
                            x=1125, y=300,
                            anchor_x='center', anchor_y='center',batch = self.batch)
        self.page_label.text = str(self.page)
        self.sprites = []

        self.current_page_sprites = []
        # Sprites in Hand
        self.sprites_hand = []
        # Adding Sprites for Page 1 & 2
        self.all_cards = list(Cards.cards.keys())[:-5]
        for i in range(len(self.all_cards)):
          if i < 16:
            self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(Cards.cards[self.all_cards[i]][6]),
                                                      self.all_card_indentation+self.position[0]+(i % self.cpr)*(135+self.gap),
                                                      self.height-(int(i/self.cpr)+1)*(135+self.gap)+self.position[1]+self.frame_height_gain))
          #Ab der 15ten Karte  fangen die Koordinaten von vorne an (Page 2)
          elif i < 31:
            self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(Cards.cards[self.all_cards[i]][6]),
                                                      self.all_card_indentation+self.position[0]+((i-16) % self.cpr)*(135+self.gap),
                                                      self.height-(int((i-16)/self.cpr)+1)*(135+self.gap)+self.position[1]+self.frame_height_gain))
      #Side Card      
        self.blank = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/blank_card.png"),1500, height //4 )
        #anchor_x = 'center', anchor_y = 'center'
        self.select_sprite = pyglet.sprite.Sprite(pyglet.image.load("resc/gray_frame.png"),self.blank.x+50, self.blank.y+220)
        # --- Card Describtion ---
        self.card_describtion_card = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            color=(109, 43, 43,255),
                            x=self.blank.x+50, y=self.blank.y+160,
                            anchor_x='left', anchor_y='top',multiline=True,width=265)
        # --- Card Name ---
        self.card_name = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=24,
                            bold=True,color=(109, 43, 43,255),
                            x=self.blank.x+self.blank.width//2, y=self.blank.y+500,
                            anchor_x='center', anchor_y='center')    
        # --- Stats Block ---
        self.card_damage = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            bold = True,color=(109, 43, 43,255),
                            x=self.blank.x+85, y=self.blank.y+205,
                            anchor_x='left', anchor_y='top')
        self.card_health = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            bold = True,color=(109, 43, 43,255),
                            x=self.blank.x+200, y=self.blank.y+205,
                            anchor_x='left', anchor_y='top')
        self.card_cost = pyglet.text.Label("",
                                font_name='Bahnschrift Light', font_size=12,
                                bold = True,color=(109, 43, 43,255),
                                x=self.blank.x+300, y=self.blank.y+205,
                                anchor_x='left', anchor_y='top')
      #  
             
    def move_card(self,x,y):
        rx = x-self.all_card_indentation-self.position[0]
        ry = (self.height+self.frame_height_gain)-(y-self.position[1])#(self.h-self.position[1])-(y-self.position[1])-self.height
        if y >=self.position[1]+self.frame_height_gain:
            rx /= (135+self.gap); ry /= (135+self.gap)
            if rx-int(rx) <= 1-self.gap/(135+self.gap): 
                if ry-int(ry) >= self.gap/(135+self.gap):
                    num = int(int(rx) + int(ry)* (self.width/(135+self.gap)-2)+(self.page-1)*16)
                    self.target = Cards.cards[self.all_cards[num]]
                    describtion = Cards.cards_describtion[self.all_cards[num]]
                    self.target.append(describtion[0]) 
                    self.target.append(self.all_cards[num])
                    self.update_card(self.target)
                    if num < len(self.all_cards) and num not in self.hand:
                        if len(self.hand) < self.max_hand_lenght:
                            #Instead of Changing Position adding Sprite to new List and Changing Position                            
                            self.sprites_hand.append(self.sprites[num])
                            self.sprites_hand[-1].y = self.position[1]
                            self.sprites_hand[-1].x = self.position[0]+(135+self.gap)*len(self.hand)                           
                            #Adding Card to Hand
                            self.hand.append(num)
                            #Replacing Index in Sprites, because of not Index Problems (num usw....)
                            self.replace_index(self.sprites,num,num)

            
        elif y <= self.position[1]+(135+self.gap)+self.gap:
            num = int((x-self.position[0])/(135+self.gap))
            rx = (x-self.position[0])/(135+self.gap)
            if rx-int(rx) >= 1-self.gap/(135+self.gap): 
                return
            if len(self.hand) > num:
                card = self.hand[num]
                # Replacing Index in sprites and changing Position
                self.replace_index(self.sprites,card,self.sprites_hand[num],pool=True)
                # Removing Card from varios Lists
                self.sprites_hand.remove(self.sprites_hand[num])
                self.hand.remove(card)

                if len(self.hand) > 0:
                    for c in range(num,len(self.hand),1):
                      self.sprites_hand[c].x -= (135+self.gap)
                  
    def press(self,x,y,button):
        if button == mouse.LEFT:
          xp,yp = self.position
          if x >= xp and x < xp+self.width and y >= yp and y < yp+self.height+self.frame_height_gain:
            #print("pressed")
            self.move_card(x,y)
            return self.action
        return None
    
    def update_page(self,page): 
      self.page += page
      self.page_label.text = str(self.page)
   
    def update_card(self,target):
      try:
          self.select_sprite.image = pyglet.image.load(target[6][:-4]+"_large.png")
      except:
          self.select_sprite.image = pyglet.image.load(target[6])
      self.card_describtion_card.text = target[10]
      self.card_name.text = target[11]
      self.card_damage.text = str(target[3])
      self.card_health.text = str(target[1])
      self.card_cost.text = str(target[4])

    def replace_index(self,liste,index,replacement,pool=False):
      liste.insert(index, replacement)
      liste.remove(liste[index+1])
      if pool:
        if index < 16:
          liste[index].y = self.height-(int(index/self.cpr)+1)*(135+self.gap)+self.position[1]+self.frame_height_gain
          liste[index].x = self.all_card_indentation+(index % self.cpr)*(135+self.gap)+self.position[0]
        elif index < 31:
          liste[index].y = self.height-(int((index-16)/self.cpr)+1)*(135+self.gap)+self.position[1]+self.frame_height_gain
          liste[index].x = self.all_card_indentation+((index-16) % self.cpr)*(135+self.gap)+self.position[0]
        
      

class CardScreenCards:
  def __init__(self,batch,width,height):
      self.hand = []#[0,1,2,3,4,5,6,7,8,9,10,11,12]#
      self.max_hand_lenght = 10
      """
      mesh:
      x,x,x,x,x    | all_cards
      x,x,x,x,x    |
      x,x,x,x,x    |
      .........    | selected
      """
      self.h = height
      self.w = width
      self.batch = batch
      
      self.all_card_indentation = 100
      self.frame_height_gain = 120
      self.gap = 20
      self.cpr = 8
      self.page = 1

      self.action = None
      self.height = 3*(135+self.gap)+self.gap   
      self.width = self.cpr*(135+self.gap)+(135+self.gap)*2
      self.position = (30,(height-self.height-450))        
      
      self.background = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/card_selection_frame.png"),self.position[0],self.position[1]+135+self.gap*2)

      self.grass_row = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/grass_row.png"),self.position[0],self.position[1])

      self.page_label = pyglet.text.Label("",
                            font_name='Times New Roman', font_size=40,
                            color=(0, 0, 0,255),
                            x=1125, y=300,
                            anchor_x='center', anchor_y='center',batch = self.batch)
      self.page_label.text = str(self.page)
      self.sprites = []
    #Side Card      
      self.blank = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/blank_card.png"),1500, height //4 )
      #anchor_x = 'center', anchor_y = 'center'
      self.select_sprite = pyglet.sprite.Sprite(pyglet.image.load("resc/gray_frame.png"),self.blank.x+50, self.blank.y+220)
      # --- Card Describtion ---
      self.card_describtion_card = pyglet.text.Label("",
                          font_name='Bahnschrift Light', font_size=12,
                          color=(109, 43, 43,255),
                          x=self.blank.x+50, y=self.blank.y+160,
                          anchor_x='left', anchor_y='top',multiline=True,width=265)
      # --- Card Name ---
      self.card_name = pyglet.text.Label("",
                          font_name='Bahnschrift Light', font_size=24,
                          bold=True,color=(109, 43, 43,255),
                          x=self.blank.x+self.blank.width//2, y=self.blank.y+500,
                          anchor_x='center', anchor_y='center')    
      # --- Stats Block ---
      self.card_damage = pyglet.text.Label("",
                          font_name='Bahnschrift Light', font_size=12,
                          bold = True,color=(109, 43, 43,255),
                          x=self.blank.x+85, y=self.blank.y+205,
                          anchor_x='left', anchor_y='top')
      self.card_health = pyglet.text.Label("",
                          font_name='Bahnschrift Light', font_size=12,
                          bold = True,color=(109, 43, 43,255),
                          x=self.blank.x+200, y=self.blank.y+205,
                          anchor_x='left', anchor_y='top')
      self.card_cost = pyglet.text.Label("",
                              font_name='Bahnschrift Light', font_size=12,
                              bold = True,color=(109, 43, 43,255),
                              x=self.blank.x+300, y=self.blank.y+205,
                              anchor_x='left', anchor_y='top')
    #  
      self.sprites = []
      
      self.all_cards = list(Cards.cards.keys())[:-5]
      for i in range(len(self.all_cards)):
        if i < 16:
          self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(Cards.cards[self.all_cards[i]][6]),
                                                    self.all_card_indentation+self.position[0]+(i % self.cpr)*(135+self.gap),
                                                    self.height-(int(i/self.cpr)+1)*(135+self.gap)+self.position[1]+self.frame_height_gain))
        #Ab der 15ten Karte  fangen die Koordinaten von vorne an (Page 2)
        elif i < 31:
          self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(Cards.cards[self.all_cards[i]][6]),
                                                    self.all_card_indentation+self.position[0]+((i-16) % self.cpr)*(135+self.gap),
                                                    self.height-(int((i-16)/self.cpr)+1)*(135+self.gap)+self.position[1]+self.frame_height_gain))
    
  def move_card(self,x,y):
      rx = x-self.all_card_indentation-self.position[0]
      ry = (self.height+self.frame_height_gain)-(y-self.position[1])#(self.h-self.position[1])-(y-self.position[1])-self.height
      if y >=self.position[1]+self.frame_height_gain:
          rx /= (135+self.gap); ry /= (135+self.gap)
          if rx-int(rx) <= 1-self.gap/(135+self.gap): 
              if ry-int(ry) >= self.gap/(135+self.gap):
                  num = int(int(rx) + int(ry)* (self.width/(135+self.gap)-2)+(self.page-1)*16)
                  self.target = Cards.cards[self.all_cards[num]]
                  describtion = Cards.cards_describtion[self.all_cards[num]]
                  self.target.append(describtion[0]) 
                  self.target.append(self.all_cards[num])
                  self.update_card(self.target)
                  
  def update_page(self,page): 
      self.page += page
      self.page_label.text = str(self.page)

  def press(self,x,y,button):
      if button == mouse.LEFT:
        xp,yp = self.position
        if x >= xp and x < xp+self.width and y >= yp and y < yp+self.height+self.frame_height_gain:
          #print("pressed")
          self.move_card(x,y)
          return self.action
      return None
  
  def update_card(self,target):
    try:
        self.select_sprite.image = pyglet.image.load(target[6][:-4]+"_large.png")
    except:
        self.select_sprite.image = pyglet.image.load(target[6])
    self.card_describtion_card.text = target[10]
    self.card_name.text = target[11]
    self.card_damage.text = str(target[3])
    self.card_health.text = str(target[1])
    self.card_cost.text = str(target[4])

class Screen:
  def draw(self):
    self.batch.draw()

  def update(self,dt):
    pass
class StartScreen(Screen):
  def __init__(self,width,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []
    
    img = pyglet.image.load("resc/jolas/Logo.png")
    img.anchor_x = img.width//2
    img.anchor_y = img.height//2

    self.map = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/map3.png"), 0, 80)

    self.logo = pyglet.sprite.Sprite(img, width/2, height/2 + 360, batch=self.batch)

    button = Button(pyglet.image.load("resc/jolas/online.png")
                    ,width/2,height/2+140,batch=self.batch)
    button.action = "ONLINE"
    self.buttons.append(button)

    button = Button(pyglet.image.load("resc/jolas/offline.png"),width/2,height/2+20,batch=self.batch)
    button.action = "StartGameOffline"
    self.buttons.append(button)
    
    button = Button(pyglet.image.load("resc/jolas/cards.png"),width/2,height/2-100,batch=self.batch)
    button.action = "CARDS"
    self.buttons.append(button)
     
    
    button = Button(pyglet.image.load("resc/jolas/settings.png"),width/2,height/2-220,batch=self.batch)
    button.action = "SETTINGS"
    self.buttons.append(button)

    button = Button(pyglet.image.load("resc/jolas/exit.png"),width/2,height/2-340,batch=self.batch)
    button.action = "QUIT"
    self.buttons.append(button)

  def draw(self):
        self.map.draw()
        self.batch.draw()
class SettingsScreen(Screen):
  def __init__(self,width,height,IP):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []
    img = pyglet.image.load("resc/jolas/settings_title.png")
    img.anchor_x = img.width//2
    img.anchor_y = img.height//2
    self.lobby_title = pyglet.sprite.Sprite(img, width/2, height/2 + 450, batch=self.batch)

    img = pyglet.image.load("resc/unactive_ip_settings.png")
    self.ip_textbox = TextBox(img,width/2-img.width/2,height/2+img.height/2,batch=self.batch)
    self.buttons.append(self.ip_textbox)
    self.ip_textbox.text = IP
 
    button = Button(pyglet.image.load("resc/notready.png"),width/2,height/2-135,batch=self.batch)
    button.action = "BACK"
    self.buttons.append(button)
    self.blink_time = 0
    
  def update(self,dt):
    if self.ip_textbox.active:
        self.blink_time += dt
        if self.blink_time >= 0.7:
            self.blink_time = 0
            self.ip_textbox.blink()
            
  def draw(self):
    self.batch.draw()
    if self.ip_textbox.active:
        self.ip_textbox.label.draw()    
class LobbyScreen(Screen):
  def __init__(self,width,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []

    self.ready = False
    self.opponent_ready = False
    
  
  
    ## hand selection -> backround frame
    ## add changeable label for opponent search
    ## change ready/ unready label accordingly
    #d# add header 
    
    self.opponent_found_img = pyglet.image.load("resc/jolas/opponent_found.png")
    self.awaiting_opponent_img = pyglet.image.load("resc/jolas/awaiting_opponent.png")

    self.ready_img = pyglet.image.load("resc/jolas/ready.png")
    self.unready_img = pyglet.image.load("resc/jolas/unready.png")

    self.opponent_search = pyglet.sprite.Sprite(self.awaiting_opponent_img, 0, height-150, batch=self.batch)

    img = pyglet.image.load("resc/jolas/your_hand.png")
    img.anchor_x = img.width//2
    img.anchor_y = img.height//2

    self.your_hand = pyglet.sprite.Sprite(img, width/2-100, 60, batch=self.batch)

    img = pyglet.image.load("resc/jolas/lobby_title.png")
    img.anchor_x = img.width//2
    img.anchor_y = img.height//2
    self.lobby_title = pyglet.sprite.Sprite(img, width/2, height/2 + 450, batch=self.batch)

    self.hand_selection = HandSelection(self.batch,width,height)
    self.buttons.append(self.hand_selection)

    #bad formating, bad layout, bad design
    #implement Castle selection!
    
    self.ready_button = Button(self.ready_img,width-300,20,batch=self.batch,
                               adj_anchor=False)
       
    self.ready_button.action = "READY"
    self.buttons.append(self.ready_button)
    
    self.back_button = Button(pyglet.image.load("resc/backArrow.png")
                              ,20,20, batch = self.batch,
                              adj_anchor=False)
    self.back_button.action = "BACK"
    self.buttons.append(self.back_button)

    self.page_foreward_button = Button(pyglet.image.load("resc\page_selector_forewards.png")
                                        ,1150,250, batch = self.batch, adj_anchor = False)
    self.page_foreward_button.action = "Page->"
    self.buttons.append(self.page_foreward_button)

    self.page_backward_button = Button(pyglet.image.load("resc\page_selector_backwards.png")
                                        ,1000,250, batch = self.batch, adj_anchor = False)
    self.page_backward_button.action = "Page<-"
    self.buttons.append(self.page_backward_button)
  
  def update_opponent_search(self,delay,lz):
    if lz != 2:
      self.opponent_search.image = self.awaiting_opponent_img
    else:
      self.opponent_search.image = self.opponent_found_img

  def update_ready_button(self,delay=None):
    if self.ready:
      self.ready_button.image = self.unready_img
    else:
      self.ready_button.image = self.ready_img
  
    
  def draw(self):
        self.hand_selection.blank.draw()
        self.hand_selection.select_sprite.draw()
        self.hand_selection.card_describtion_card.draw()
        self.hand_selection.card_name.draw()
        self.hand_selection.card_damage.draw()
        self.hand_selection.card_health.draw()
        self.hand_selection.card_cost.draw()
        self.hand_selection.background.draw()
        self.hand_selection.grass_row.draw()
        #Drawing Sprites of Cards for Page 1,2 and hand
        if self.hand_selection.page == 1:
          for sprite in self.hand_selection.sprites[:16-len(self.hand_selection.sprites)]:
            try:
              sprite.draw()
            except:
              pass
        elif self.hand_selection.page == 2:
          for sprite in self.hand_selection.sprites[16:]:
            try:
              sprite.draw()
            except:
              pass
        for sprite in self.hand_selection.sprites_hand:
          if sprite != type(int):  
            sprite.draw()
        self.batch.draw()

class CardScreen(Screen):
  def __init__(self,width,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []

    self.ready = False
    self.opponent_ready = False
    
  
  
    ## hand selection -> backround frame
    ## add changeable label for opponent search
    ## change ready/ unready label accordingly
    #d# add header 
    

    img = pyglet.image.load("resc/jolas/your_hand.png")
    img.anchor_x = img.width//2
    img.anchor_y = img.height//2

    img = pyglet.image.load("resc/jolas/card_view_title.png")
    img.anchor_x = img.width//2
    img.anchor_y = img.height//2
    self.lobby_title = pyglet.sprite.Sprite(img, width/2, height/2 + 450, batch=self.batch)

    self.hand_selection = CardScreenCards(self.batch,width,height)
    self.buttons.append(self.hand_selection)

    #bad formating, bad layout, bad design
    #implement Castle selection!
       
    self.back_button = Button(pyglet.image.load("resc/backArrow.png")
                              ,20,20, batch = self.batch,
                              adj_anchor=False)
    self.back_button.action = "BACK"
    self.buttons.append(self.back_button)   
    self.page_foreward_button = Button(pyglet.image.load("resc\page_selector_forewards.png")
                                        ,1150,250, batch = self.batch, adj_anchor = False)
    self.page_foreward_button.action = "Page->"
    self.buttons.append(self.page_foreward_button)

    self.page_backward_button = Button(pyglet.image.load("resc\page_selector_backwards.png")
                                        ,1000,250, batch = self.batch, adj_anchor = False)
    self.page_backward_button.action = "Page<-"
    self.buttons.append(self.page_backward_button)
  
  def draw(self):
    self.hand_selection.blank.draw()
    self.hand_selection.select_sprite.draw()
    self.hand_selection.card_describtion_card.draw()
    self.hand_selection.card_name.draw()
    self.hand_selection.card_damage.draw()
    self.hand_selection.card_health.draw()
    self.hand_selection.card_cost.draw()
    self.hand_selection.background.draw()
    #Drawing Sprites of Cards for Page 1,2 and hand
    if self.hand_selection.page == 1:
      for sprite in self.hand_selection.sprites[:16-len(self.hand_selection.sprites)]:
        try:
          sprite.draw()
        except:
          pass
    elif self.hand_selection.page == 2:
      for sprite in self.hand_selection.sprites[16:]:
        try:
          sprite.draw()
        except:
          pass
    self.batch.draw()
   