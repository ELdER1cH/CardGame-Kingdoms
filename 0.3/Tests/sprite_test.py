import pyglet

class Window(pyglet.window.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.sprite = pyglet.sprite.Sprite(pyglet.image.load("Bomb.png"),0,0)
    pyglet.clock.schedule(self.update)
  def on_draw(self):
    self.clear()
    self.sprite.draw()

  def update(self,dt):
    self.sprite.position = (1,1)

if __name__ == "__main__":
  window = Window()
  pyglet.app.run()
