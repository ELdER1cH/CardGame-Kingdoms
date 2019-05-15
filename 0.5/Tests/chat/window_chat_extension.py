import pyglet

class Window(pyglet.window.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    pyglet.gl.glClearColor(255,255,255,255)
    self.sprite2 = pyglet.sprite.Sprite(pyglet.image.load("palatin.png"),100,0)

  def on_draw(self):
    self.clear()
    self.sprite2.draw()

if __name__ == "__main__":
  window = Window(400,400,"Chat Test")
  
  pyglet.app.run()
