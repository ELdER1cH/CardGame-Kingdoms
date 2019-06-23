import pyglet

##für irgendwann.. vielleicht nie - ist unnötig

class Layout:
  def __init__(self,layout):
    self.layout = layout

  def button(self,width,height):
    if self.layout == "classic":
      img = pyglet.image.load("Castle.png")
      x = 10
      y = 10
      return img, x,y
