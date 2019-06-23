import screens
import pyglet
from pyglet.gl import *
import client
import threading
import json
import time

VERSION = "0.134.0"
IP = 'localhost'
PORT = 8765
#add loading screen between screen switches (/blank/ anim)

class Window(pyglet.window.Window):
  def __init__(self,*args):
    super().__init__(*args,vsync=True)
    self.current_screen = screens.StartScreen(self.width,self.height)
    self.hover_frame = pyglet.sprite.Sprite(pyglet.image.load("gray_frame.png"),
                                            0,-100)

    #pyglet.clock.schedule_interval(self.update,1/10)
    pyglet.clock.schedule(self.update)
    #self.version = self.mana_label = pyglet.text.Label("version: "+VERSION,
    #                      font_name='Times New Roman',
    #                      font_size=12,
    #                      bold=True,color=(0, 0, 0,195),
    #                      x=20, y=20)

  def back(self,delay):
    self.current_screen = screens.StartScreen(self.width,self.height)
    
  def receive_messages(self):
    try: 
      while True:
        r = json.loads(self.client.s.recv(4096).decode())
        print("<< received %s" % r)
        if type(r) == dict: 
            if r['type'] == 'replace': #cardnum,pos
              pyglet.clock.schedule_once(self.current_screen.batch.replace(
                r['replace'][0],r['replace'][1]),0.1)
            elif r['type'] == 'swap': #pos1,pos2
              pyglet.clock.schedule_once(self.current_screen.batch.place(
                r['swap'][0],r['swap'][1]),0.1)
            elif r['type'] == 'attack': #pos1,pos2
              pyglet.clock.schedule_once(self.current_screen.batch.place(
                r['attack'][0],r['attack'][1]),0.1)
            
            elif r['type'] == 'lobby':
              self.client.lobby = int(r['lobby'])
              self.client.lobbysize = int(r['lobbysize'])
              
              if self.client.lobbysize == 2:
                self.current_screen.ready_button.action = "READY"
              else:
                self.current_screen.ready_button.action = None
                self.current_screen.ready = False
                self.current_screen.opponent_ready = False
                
              self.client.send_lobby()
              print(f"<< lobby update: {self.client.lobby} (size: {self.client.lobbysize})")
              self.current_screen.lobby_text = ("lobby: %s (size: %s)" %
                                           (r['lobby'],r['lobbysize']))
              self.current_screen.laststatus_text = ">> new connection to lobby!"
              pyglet.clock.schedule_once(self.current_screen.update_label,0.1)

            elif r['type'] == 'ready':
              try:
                self.current_screen.opponent_ready = not self.current_screen.opponent_ready
                self.current_screen.ready = r['ready']
                if self.current_screen.ready and self.current_screen.opponent_ready:
                  self.start_game()
              except:
                print("<< r['ready'] received a message for an action that could not be executed!")
                
    except ConnectionResetError as err:
      print(err)
      pyglet.clock.schedule_once(self.back,0.1)
      
  def update(self,dt):
    self.current_screen.update(dt)

  def start_game(self):
    print('this should now start the game')

  def on_draw(self):
    self.clear()
    self.current_screen.draw()
    self.hover_frame.draw()
    #self.version.draw()
    fps_display.draw()
    
  def on_mouse_press(self,x,y,button,mod):
    action = self.current_screen.mouse_press(x,y,button)
    if action != None:
      if action == "ONLINE":
        self.current_screen = screens.LobbyScreen(self.width,self.height,
                                                  "pending...",
                                                  "pending...",
                                                  IP,PORT)
        try:
          self.client = client.Client(IP,PORT)
        except Exception as err:
          print(err)
          print("<> connection could not be established!")
          self.current_screen = screens.StartScreen(self.width,self.height)
          return
        threading.Thread(target=self.receive_messages).start()
        
      elif action == "BACK":
        self.current_screen = screens.StartScreen(self.width,self.height)
      elif action == "OFFLINE":
        print('not featured yet')
      elif action == "SETTINGS":
        self.current_screen = screens.SettingsScreen(self.width,self.height)
      elif action == "QUIT":
        self.close()
      elif action == "READY":
        self.current_screen.ready_button.action = "NOTREADY"
        self.current_screen.ready_button.image = pyglet.image.load('ready.png')
        self.current_screen.laststatus.text = "<> readied"
        self.current_screen.ready = True
        self.client.send_ready(self.current_screen.opponent_ready)
        if self.current_screen.ready and self.current_screen.opponent_ready:
          self.start_game()
        return
      elif action == "NOTREADY":
        self.current_screen.ready_button.action = "READY"
        self.current_screen.ready_button.image = pyglet.image.load('notready.png')
        self.current_screen.laststatus.text = "<> un-readied"
        self.current_screen.ready = False
        self.client.send_ready(self.current_screen.opponent_ready)
        return
      self.hover_frame.image.width = 350
      self.hover_frame.image.height = 100
      self.hover_frame.position = (0,-200)
      #loading.. screen
      #switch current_screen

  def on_mouse_motion(self,x,y,dx,dy):
    info = self.current_screen.mouse_motion(x,y,dx,dy)
    if info != None:
      self.hover_frame.image.width = info[1]
      self.hover_frame.image.height = info[2]
      self.hover_frame.position = info[0]

  def on_close(self):
    try:
      self.client.s.close()
    except:
      pass

if __name__ == "__main__":
  window = Window(720,800,"Client Stucture")
  glClearColor(0.6,0.6,0.85,1)
  fps_display = pyglet.window.FPSDisplay(window)
  pyglet.app.run()
