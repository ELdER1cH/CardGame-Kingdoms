try:
  import pyglet
  from pyglet.gl import *
  import pop_up, Batch, Cards, Card,Window
  from pyglet.window import key, mouse
  from Window import Window
  from Startscreen import Startscreen
  import chat_dependencies.main_chat as main_chat
  import random
except ImportError as err:
  print("couldn't load modue. %s" % (err))

val = 1
SPRITE_WIDTH = int(120/val)
SPRITE_HEIGHT = int(100/val)
INDENTATION_RIGHT = 2


if __name__ == "__main__":
  width = 600+120*INDENTATION_RIGHT;height =800
  window = Startscreen(width,height,"New Stucture Testing",resizable=True,vsync=False)
  glClearColor(135,206,250,255)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  fps_display = pyglet.window.FPSDisplay(window)
  fps_display.label.font_size = 15
  pyglet.app.run()
