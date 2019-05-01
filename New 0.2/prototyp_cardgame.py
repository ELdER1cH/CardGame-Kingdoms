import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Window

#einnehmen von feldern/ feldarten - aqua/violett/grau(unbesetzt)
#kampfsystem
#mehr Karten + goldener Stapel

#stats/ anzeigen - leben, stats truppen z.b. von letztem select
#-hover funktion

#evtl. 2./ 2.0 prototyp
#besseres mapping
#inventar schrumpfen
#mehrere Karten pro Feld

#done: Code reinigen, automatisch nachfüllen, rounds -player bezogen arbeiten xD


if __name__ == "__main__":
    window = Window.Window(600,900,'Prototyp')
    glClearColor(0.9,0.9,1,1)
    pyglet.app.run()

