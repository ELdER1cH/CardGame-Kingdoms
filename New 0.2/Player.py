import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Window, Map ,card


class Player:
    def __init__(self):
        self.map = Map.Map()