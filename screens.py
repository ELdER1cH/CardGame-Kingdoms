import pyglet
from pyglet.window import mouse, key
import Cards

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
        
        self.all_cards = list(Cards.cards.keys())[:-4]
        for i in range(len(self.all_cards)):
            self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(Cards.cards[self.all_cards[i]][6]),
                                                     self.indentation+(i % self.cpr)*(120+self.gap),
                                                     height-(int(i/self.cpr)+1)*(100+self.gap),batch=batch))
            
    def move_card(self,x,y):
        #rx & ry werden angepasst, dass sie am Rand des Kartenauswahlfelds beginnen und nicht am Rand des Fensters 
        rx = x-self.indentation
        ry = y-(self.h-self.height)
        #wenn eine Karte der Hand hinzugefügt werden soll - Klick in kartenauswahl  
        if y >= self.h-3*(100+self.gap):
            # rx wird geteilt - soll maximal 5 (bzw. 0-4) sein, weil es 5 Karten pro Reihe gibt
            rx /= (120+self.gap); ry = (self.height-ry)/(100+self.gap)
            # wenn der click nicht zwischen den Karten war 
            if rx-int(rx) <= 1-self.gap/(120+self.gap): 
                if ry-int(ry) >= self.gap/(100+self.gap):
                    # Testet in welcher Reihe geklickt wurde und setzt je nachdem num fest
                      # Num Calc: Karten Nummer wird anhand der Stelle und Reihe bestimmt (Zahl von 0-4 + (0-2 für die Reihe * 5 Karten pro Reihe)
                    #Reihe 1
                    if int(int(ry)* self.width/(120+self.gap)-1) < 5:
                      num = int(int(rx) + int(ry)* self.width/(120+self.gap)) 
                    #Reihe 2
                    elif   int(int(ry)* self.width/(120+self.gap)-1) < 11:  
                      num = int(int(rx) + int(ry)* self.width/(120+self.gap)-1)
                    #Reihe 3
                    else:
                      num = int(int(rx) + int(ry)* self.width/(120+self.gap)-2)    
                    # wenn die Nummer nicht größer als alle Karten ist & und die Nummer noch nicht in die Hand gewählt wurde 
                    if num < len(self.all_cards) and num not in self.hand:
                        #wenn Die Hand nicht schon voll ist 
                        if len(self.hand) < self.max_hand_lenght:
                            # Karte nach unten in seinen Platz in der Hand schieben
                            self.sprites[num].y = self.position[1]
                            self.sprites[num].x = (120+self.gap)*len(self.hand)#+self.indentation
                            self.hand.append(num)
        # wenn der Klick bei den schon ausgewählten Karten war    
        elif y <= self.h-3*(100+self.gap)-self.gap:
            # num ist wieder die Stelle in der Reihe - bloß gibt es nur eine Reihe
            num = int(x/(120+self.gap))
            rx = x/(120+self.gap)
            # Lücken Check - soll nicht dazwischen sein 
            if rx-int(rx) >= 1-self.gap/(120+self.gap): 
                return
            # wenn alles passt die Karte wieder aus der Hand entfernen und an den alten Platz ziehen     
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

    button = Button(pyglet.image.load("resc/online_button.png")
                    ,width/2,height/2+240,batch=self.batch)
    button.action = "ONLINE"
    self.buttons.append(button)

    button = Button(pyglet.image.load("resc/offline_button.png"),width/2,height/2+120,batch=self.batch)
    button.action = "OFFLINE"
    self.buttons.append(button)
    
    button = Button(pyglet.image.load("resc/settings_button.png"),width/2,height/2,batch=self.batch)
    button.action = "SETTINGS"
    self.buttons.append(button)

    button = Button(pyglet.image.load("resc/quit_button.png"),width/2,height/2-120,batch=self.batch)
    button.action = "QUIT"
    self.buttons.append(button)

class SettingsScreen(Screen):
  def __init__(self,width,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []
    
    img = pyglet.image.load("resc/Castle.png")
    button = Button(img,width/2,height/2,batch=self.batch)
    button.action = "BACK"
    self.buttons.append(button)
    
class LobbyScreen(Screen):
  def __init__(self,width,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []

    self.ready = False
    self.opponent_ready = False
    
    self.hand_selection = HandSelection(self.batch,width,height)
    self.buttons.append(self.hand_selection)

    #bad formating, bad layout, bad design
    #implement Hand selection!
    #implement Castle selection!
    
    self.ready_button = Button(pyglet.image.load("resc/ready.png")
                               ,width-120,20,batch=self.batch,
                               adj_anchor=False)
    
    self.ready_button.action = "READY"
    
    #self.ready_button.action = "READY"
    self.buttons.append(self.ready_button)
