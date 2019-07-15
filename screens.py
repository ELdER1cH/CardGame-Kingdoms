import pyglet
from pyglet.window import mouse, key
from main import Window
import Cards
from pyglet.gl import *

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
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
        self.max_hand_lenght = 6
        """
        mesh:
        x,x,x,x,x    | all_cards
        x,x,x,x,x    |
        x,x,x,x,x    |
        .........    | selected
        """
        self.h = height
        self.w = width
        
        self.indentation = 100
        self.gap = 20
        self.cpr = 5
        
        self.action = None
        self.height = 4*(100+self.gap)+self.gap    
        self.width = self.cpr*(120+self.gap)+(120+self.gap)
        self.position = (0,(height-self.height))        
        
        self.sprites = []
        
        self.all_cards = list(Cards.cards.keys())[:-5]
        for i in range(len(self.all_cards)):
            self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(Cards.cards[self.all_cards[i]][6]),
                                                     self.indentation+(i % self.cpr)*(120+self.gap),
                                                     height-(int(i/self.cpr)+1)*(100+self.gap),batch=batch))
            
    def move_card(self,x,y):
        rx = x-self.indentation
        ry = y-(self.h-self.height)
        if y >= self.h-3*(100+self.gap):
            rx /= (120+self.gap); ry = (self.height-ry)/(100+self.gap)
            if rx-int(rx) <= 1-self.gap/(120+self.gap): 
                if ry-int(ry) >= self.gap/(100+self.gap):
                    num = int(int(rx) + int(ry)* (self.width/(120+self.gap)-1))
                    if num < len(self.all_cards) and num not in self.hand:
                        if len(self.hand) < self.max_hand_lenght:
                            self.sprites[num].y = self.position[1]
                            self.sprites[num].x = (120+self.gap)*len(self.hand)#+self.indentation
                            self.hand.append(num)
            
        elif y <= self.h-3*(100+self.gap)-self.gap:
            num = int(x/(120+self.gap))
            rx = x/(120+self.gap)
            if rx-int(rx) >= 1-self.gap/(120+self.gap): 
                return
            if len(self.hand) > num:
                card = self.hand[num]
                self.sprites[card].y = self.h-(int(card/self.cpr)+1)*(100+self.gap)
                self.sprites[card].x = self.indentation+(card % self.cpr)*(120+self.gap)
                
                self.hand.remove(card)
                
                if len(self.hand) > 0:
                    for c in self.hand[num:]:
                        self.sprites[c].x -= (120+self.gap)
            
    def press(self,x,y,button):
        if button == mouse.LEFT:
          xp,yp = self.position
          if x >= xp and x < xp+self.width and y >= yp and y < yp+self.height:
            #print("pressed")
            self.move_card(x,y)
            return self.action
        return None

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

    self.map = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/map.png"), 0, 80)

    self.logo = pyglet.sprite.Sprite(img, width/2, height/2 + 360, batch=self.batch)

    button = Button(pyglet.image.load("resc/jolas/online.png")
                    ,width/2,height/2+140,batch=self.batch)
    button.action = "ONLINE"
    self.buttons.append(button)

    button = Button(pyglet.image.load("resc/jolas/offline.png"),width/2,height/2+20,batch=self.batch)
    button.action = "OFFLINE"
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
    
    img = pyglet.image.load("resc/unactive_ip_settings.png")
    self.ip_textbox = TextBox(img,width/2-img.width/2,height/2+img.height/2,batch=self.batch)
    self.buttons.append(self.ip_textbox)
    self.ip_textbox.text = IP
 
    button = Button(pyglet.image.load("resc/notready.png"),width/2,height/2-120,batch=self.batch)
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
    
    self.hand_selection = HandSelection(self.batch,width,height)
    self.buttons.append(self.hand_selection)

    #bad formating, bad layout, bad design
    #implement Castle selection!
    
    self.ready_button = Button(pyglet.image.load("resc/ready.png")
                               ,width-120,20,batch=self.batch,
                               adj_anchor=False)
       
    self.ready_button.action = "READY"
    self.buttons.append(self.ready_button)
    
    self.back_button = Button(pyglet.image.load("resc/backArrow.png")
                              ,20,20, batch = self.batch,
                              adj_anchor=False)
    self.back_button.action = "BACK"
    self.buttons.append(self.back_button)

class OfflineScreen(Screen):
  def __init__(self,width, height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []

    self.ready = False
    self.opponent_ready = False


    self.label = pyglet.text.Label(text= 'Start',
                          x = width//2, 
                          y = height//2,
                          font_name='Times New Roman',
                          font_size=48,
                          bold=True,
                          color=(0, 0, 0,255),
                          batch= self.batch, anchor_x = 'center',anchor_y= 'center'
                    
                          )  
    self.back_button = Button(pyglet.image.load("resc/backArrow.png")
                          ,20,20, batch = self.batch,
                          adj_anchor=False)
    self.ready_button = Button(pyglet.image.load("resc/ready.png")
                               ,width-120,20,batch=self.batch,
                               adj_anchor=False)
    self.ready_button.action = "StartGameOffline"
    self.back_button.action = "BACK"
    self.buttons.append(self.ready_button)
    self.buttons.append(self.back_button)
