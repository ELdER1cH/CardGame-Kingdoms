import pyglet
import client
import threading
from pyglet.window import mouse, key
import json
from math import *
from pyglet.gl import *

IP = 'localhost'
PORT = 8765

def makeCircle(numPoints,xy):
    verts = []
    for i in range(numPoints):
        angle = radians(float(i)/numPoints * 360.0)
        x = 5*cos(angle) + xy[0]
        y = 5*sin(angle) + xy[1]
        verts += [x,y]
    
    return pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
 
class Window(pyglet.window.Window):
  def __init__(self,*args):
    super().__init__(*args)
    self.client = client.Client(IP,PORT)
    self.height = 200
    self.width = 100
    
    threading.Thread(target=self.receive_messages).start()
  
    self.pos = (10,10)
    self.circle = makeCircle(5,self.pos)
    
    pyglet.clock.schedule(self.update)

  def update(self,dt):
    self.circle = makeCircle(10,self.pos)

  def receive_messages(self):
    while True:
      r = json.loads(self.client.s.recv(4096).decode())
      print("<< received %s" % r)
      if type(r) == dict: 
          if r['type'] == 'cords': #and r['lobby'] == self.client.lobby:
            self.pos = r['cords']
          #elif r['type'] == 'users':
            #print(f"<< received {r['users']}")
          elif r['type'] == 'lobby':
            self.client.lobby = int(r['lobby'])
            self.client.send()
            print(f"<< your lobby was changed to: {self.client.lobby}")
    
  def on_draw(self):
    self.clear()
    self.circle.draw(GL_POINTS)

  def on_mouse_press(self,x,y,button,mod):
    if button == mouse.LEFT:
      self.client.CORDS['cords'] = (x,y)
      self.client.send()

if __name__ == "__main__":
  window = Window()
  pyglet.gl.glClearColor(0,0,0,1)
  pyglet.app.run()

  
  
