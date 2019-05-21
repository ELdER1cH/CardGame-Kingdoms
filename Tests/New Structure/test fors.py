class Test:
  def test(card):
    print(card.name)

class ITest:
  def __init__(self):
    self.name = "arnolrd"
    self.specials = Test()
    self.specials.test(self)
#ITest()
    
"""def fors():
  for i in range(10):
    if i >= 5:
      return
    
  for i in range(10):
    print(i)

fors()

import copy, pyglet
from pyglet.gl import *

class TestClass:
  def __init__(self):
    print("__init__")

class Once(TestClass):
  print('once?')
  def __init__(self):
    super().__init__()
    self.lis = []
    self.lis.append("zero")
    self.o = copy.deepcopy(self)
    self.lis[0] = "0"
    print(self.o.lis)
    print(self.lis)

#Once()
#Once()
#Once()

base = pyglet.image.load("Castle.png").get_image_data()
texture = pyglet.image.Texture.create(width=120,height=100)
img = pyglet.image.load("yellow_frame.png").get_image_data()
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
texture.blit_into(base,x=0, y=0, z=0)
img.blit_to_texture(texture.target,0,0, 0, z=1)
#texture.blit_into(img, x=0, y=0, z=1)
texture.save('test_merge.png')"""
