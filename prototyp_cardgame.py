import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
import Game

#mehr Karten + goldener Stapel
#einnehmen von feldern/ feldarten - aqua/violett/grau(unbesetzt)
#kampfsystem

#stats/ anzeigen - leben, stats truppen z.b. von letztem select
#-hover funktion

#evtl. 2./ 2.0 prototyp
#besseres mapping
#inventar schrumpfen
#mehrere Karten pro Feld
#spiel/level speicher funktion
#start & auswahl bildschirm
#tote karten endgültig löschen

#done: Code reinigen, automatisch nachfüllen, rounds -player bezogen arbeiten xD
#Mana, Stats, neue "cards"


if __name__ == "__main__":
    window = Game.Game(840,900,'Prototyp')
    glClearColor(0.9,0.9,1,1)
    pyglet.app.run()
