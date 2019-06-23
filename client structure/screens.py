import pyglet
from pyglet.window import mouse, key

class Button(pyglet.sprite.Sprite):
  def __init__(self,img,*args,adj_anchor=True,**kwargs):
    if adj_anchor:
      img.anchor_x = img.width//2
      img.anchor_y = img.height//2
    super().__init__(img,*args,**kwargs)
    self.onmo = False
    self.action = None

  def press(self,x,y,button):
    if button == mouse.LEFT:
      xp,yp = self.position
      xp -= self.image.anchor_x; yp -= self.image.anchor_y
      if x >= xp and x < xp+self.width and y >= yp and y < yp+self.height:
        return self.action
    return None

  def motion(self,x,y):
    xp,yp = self.position
    xp -= self.image.anchor_x; yp -= self.image.anchor_y
    if x >= xp and x < xp+self.width and y >= yp and y < yp+self.height:
      if not self.onmo:
        self.onmo = True
        return [(self.x-self.image.anchor_x,self.y-self.image.anchor_y),
                self.width,self.height]
    elif self.onmo:
      self.onmo = False
      return [(0,-self.height-self.image.anchor_y),self.width,self.height]
      

class Screen:
  def draw(self):
    self.batch.draw()

  def update(self,dt):
    pass
    
  def mouse_press(self,x,y,button):
    #for button in batch
    for b in self.buttons:
      action = b.press(x,y,button)
      if action != None:
        return action
    #return self.button.press(x,y,button)

  def mouse_motion(self,x,y,dx,dy):
    for b in self.buttons:
      #b.motion(x,y)
      action = b.motion(x,y)
      if action != None:
        return action

class StartScreen(Screen):
  def __init__(self,widht,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []
        
    img = pyglet.image.load("Castle.png")
    button = Button(pyglet.image.load("online_button.png")
                    ,widht/2,height/2+240,batch=self.batch)
    button.action = "ONLINE"
    self.buttons.append(button)

    button = Button(pyglet.image.load("offline_button.png"),widht/2,height/2+120,batch=self.batch)
    button.action = "OFFLINE"
    self.buttons.append(button)
    
    button = Button(pyglet.image.load("settings_button.png"),widht/2,height/2,batch=self.batch)
    button.action = "SETTINGS"
    self.buttons.append(button)

    button = Button(pyglet.image.load("quit_button.png"),widht/2,height/2-120,batch=self.batch)
    button.action = "QUIT"
    self.buttons.append(button)

class SettingsScreen(Screen):
  def __init__(self,widht,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []
    
    img = pyglet.image.load("Castle.png")
    button = Button(img,widht/2,height/2,batch=self.batch)
    button.action = "BACK"
    self.buttons.append(button)

class LoadingScreen(Screen):
  def __init__(self,widht,height,text):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []
    
    self.loading = pyglet.text.Label(text,x=widht/2,y=height/2,
                                     font_size=32,batch=self.batch,
                                     anchor_x="center")
    
class LobbyScreen(Screen):
  def __init__(self,widht,height,lobby,lobbysize,ip,port):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []

    if lobbysize == 2: #and len(self.hand_selection.hand) == 7
      #and self.castle_selection.castle != None
      self.ready_button.action = "READY"

    self.hand = [0,1,2,3,4,5,6]
    self.ready = False
    self.opponent_ready = False
    self.lobby_text = ""
    self.laststatus_text = ""

    #bad formating, bad layout, bad design
    #implement Hand selection!
    #implement Castle selection!
    self.opponentid = pyglet.text.Label("opponent id: unasigned",
                                      x=10,y=38,batch=self.batch)  
    self.playerid = pyglet.text.Label("player id: unasigned",
                                      x=10,y=50,batch=self.batch)
    self.lobby = pyglet.text.Label("lobby: "+str(lobby),
                                   x=10,y=62,batch=self.batch)
    self.laststatus = pyglet.text.Label("<> connected to: " + ip+ ":"+ str(port),
                                      x=10,y=10,batch=self.batch)
    self.ready_button = Button(pyglet.image.load("notready.png")
                               ,widht-120,20,batch=self.batch,
                               adj_anchor=False)

    self.hand_selection = pyglet.text.Label("hand selection - not implemented yet",
                                      x=40,y=height/2+60,batch=self.batch)

    self.castle_selection = pyglet.text.Label("castle selection - not implemented yet",
                                      x=40,y=height/2-60,batch=self.batch)
    
    #self.ready_button.action = "READY"
    self.buttons.append(self.ready_button)

  def update_label(self,delay):
    self.lobby.text = self.lobby_text
    self.laststatus.text = self.laststatus_text
