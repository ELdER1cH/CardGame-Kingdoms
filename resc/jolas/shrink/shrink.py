import pyglet
from PIL import Image
from pyglet.gl import *
import glob, os

for infile in glob.glob("*.jpg"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.resize((135,135),Image.ANTIALIAS)
      img.save("done/" + file+".png", "PNG")
      print(file)
