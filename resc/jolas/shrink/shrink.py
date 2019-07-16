import pyglet
from PIL import Image
from pyglet.gl import *
import glob, os

for infile in glob.glob("*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.resize((img.width//2,img.height//2),Image.ANTIALIAS)
      img.save("done/" + file+".png", "PNG")
      print(file)