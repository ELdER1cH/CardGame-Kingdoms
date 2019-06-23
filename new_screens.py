import pyglet
from pyglet.window import mouse, key

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

class Screen:
  def draw(self):
    self.batch.draw()

  def update(self,dt):
    pass

class StartScreen(Screen):
  def __init__(self,widht,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []

    button = Button(pyglet.image.load("resc/online_button.png")
                    ,widht/2,height/2+240,batch=self.batch)
    button.action = "ONLINE"
    self.buttons.append(button)

    button = Button(pyglet.image.load("resc/offline_button.png"),widht/2,height/2+120,batch=self.batch)
    button.action = "OFFLINE"
    self.buttons.append(button)
    
    button = Button(pyglet.image.load("resc/settings_button.png"),widht/2,height/2,batch=self.batch)
    button.action = "SETTINGS"
    self.buttons.append(button)

    button = Button(pyglet.image.load("resc/quit_button.png"),widht/2,height/2-120,batch=self.batch)
    button.action = "QUIT"
    self.buttons.append(button)

class SettingsScreen(Screen):
  def __init__(self,widht,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []
    
    img = pyglet.image.load("resc/Castle.png")
    button = Button(img,widht/2,height/2,batch=self.batch)
    button.action = "BACK"
    self.buttons.append(button)
    
class LobbyScreen(Screen):
  def __init__(self,widht,height):
    self.batch = pyglet.graphics.Batch()
    self.buttons = []

    self.hand = [0,1,2,3,4,5,6]
    self.ready = False
    self.opponent_ready = False

    #bad formating, bad layout, bad design
    #implement Hand selection!
    #implement Castle selection!
    
    self.ready_button = Button(pyglet.image.load("resc/ready.png")
                               ,widht-120,20,batch=self.batch,
                               adj_anchor=False)
    
    self.ready_button.action = "READY"
    
    #self.ready_button.action = "READY"
    self.buttons.append(self.ready_button)
