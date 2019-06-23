import new_screens as screens
import pyglet
from pyglet.gl import *
import new_client as client
import threading
import json
import time

IP = 'localhost'
PORT = 8765

class Window(pyglet.window.Window):
  def __init__(self,*args):
    super().__init__(*args)
    self.current_screen = screens.StartScreen(self.width,self.height)
    pyglet.clock.schedule(self.update)
    
  def update(self,dt):
    self.current_screen.update(dt)
  
  def on_close(self):
    super().on_close()
    print('quit!')
    try:
      self.client.s.close()
    except:
      pass

  def on_draw(self):
      self.clear()
      self.current_screen.draw()

  def start_game(self):
    print('start game here!')

  def back(self,delay):
    self.current_screen = screens.StartScreen(self.width,self.height)

  def receive_messages(self):
      while True:
        try:
          r = json.loads(self.client.s.recv(4096).decode())
          #print("<< received %s" % r)
          if type(r) == dict:
            if r['type'] == 'cords': 
              self.pos = r['cords']
            #elif r['type'] == 'users':
              #print(f"<< received {r['users']}")
            elif r['type'] == 'lobby':
              self.client.lobby = int(r['lobby'])
              self.client.lobbysize = int(r['lobbysize'])
              self.current_screen.ready = False
              self.current_screen.opponent_ready = False
              self.client.send_lobby()
              print(f"<< lobby update: {self.client.lobby} (size: {self.client.lobbysize})")
            elif r['type'] == 'ready':
              try:
                self.current_screen.opponent_ready = not self.current_screen.opponent_ready
                self.current_screen.ready = r['ready']
                print("mr: %s or: %s" %
                      (self.current_screen.ready, self.current_screen.opponent_ready))
                if self.current_screen.ready and self.current_screen.opponent_ready:
                  self.start_game()
              except:
                print("<< r['ready'] received a message for an action that could not be executed!")

        except ConnectionResetError as err:
          print(err)
          pyglet.clock.schedule_once(self.back,0.1)
          break


  def on_mouse_press(self,x,y,button,mod):
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
              self.start_game()

if __name__ == "__main__":
  window = Window(720,800,"Cardgame - Online Version (developer build)")
  glClearColor(0.5,0.5,0.5,1.0)
  pyglet.app.run()
