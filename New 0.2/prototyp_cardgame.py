import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Window, Map , Player, card

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#rounds -player bezogen arbeiten xD
#einnehmen von feldern/ feldarten - aqua/violett/grau(unbesetzt)
#kampfsystem
#automatisch nachfüllen + mehr Karten + goldener Stapel

#stats/ anzeigen - leben, stats truppen z.b. von letztem select
#-hover funktion

#evtl. 2./ 2.0 prototyp
#besseres mapping
#inventar schrumpfen
#mehrere Karten pro Feld


if __name__ == "__main__":
    window = Window.Window(600,900,'Prototyp')
    glClearColor(0.9,0.9,1,1)
    pyglet.app.run()

