# Cardgame
Spiel mit Elementen aus Karten-, Strategiespielen, sowie Schach.

##Installation
-Benötigt Python 3.x (3.6, 3.7 wurden getestet) 
	Installation via https://www.python.org/
-Benötigt pyglet v1.3.2
	Installation via pip in der Eingabeaufforderung (cmd/ Command Prompt) -> "pip install pyglet==1.3.2"
	("pip install pyglet" alleine würde eine neuere Version (derzeit v1.4.2) installieren, 
	welche nicht mit diesem Programm harmoniert - wichtige Funktionen wurden unersichtlich geändert)

## Ziel des Spiels

Ziel des Spieles ist es die gegnerische Burg zu zerstören.

## Zugablauf

1. Karten platzieren
2. Karten bewegen / Felder einnehmen / Gegnerische Karten angreifen
3. Zug beenden

### 1. Karten platzieren

Als erstes musst du Karten auf dem Spielfeld platzieren.Jede Karte kostet eine gewisse Menge an Mana.
#### Mana Regeneration
Neues Mana wird jedes mal generiert, wenn du am Zug bist.
Deine Manaregeneration setzt sich aus allen von dir eingenommen Felder, minus die Felder auf denen eine Karte liegt. 

Aber Achtung, manche Karten wirken sich nicht auf die Manaregeneration aus!
### Karten

![Karten](https://github.com/ELdER1cH/Cardgame/blob/master/resc/Karten.PNG)

####Bauernhof
- Erhöht maximales Mana um 5
- Erhöht Mana Regeneration um 2
