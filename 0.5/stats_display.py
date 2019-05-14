import pyglet

class Stats_Display():
    def __init__(self):
        #self.document = pyglet.text.document.FormattedDocument('This is a multi line document. This is a multi line document.')
        #self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255)))
        #self.text = pyglet.text.layout.TextLayout(self.document,240,420,multiline=True)
        self.select_sprite = pyglet.sprite.Sprite(pyglet.image.load('resc/card_one.png'),660, 700)
        self.mana_label = pyglet.text.Label("",
                          font_name='Times New Roman',
                          font_size=12,
                          bold=True,color=(109, 43, 43,255),
                          x=720, y=890,
                          anchor_x='center', anchor_y='top',multiline=True,width=220)
        self.card_label = pyglet.text.Label("",
                          font_name='Times New Roman',
                          font_size=12,
                          bold=True,color=(109, 43, 43,255),
                          x=660, y=700,
                          anchor_x='center', anchor_y='top',multiline=True,width=180)
        

    def update(self,mana,max_mana,mana_reg,mapp,select):
        self.mana_label.text = """
        Mana: %s
        Max Mana: %s
        Mana Reg: %s""" % (mana,max_mana,mana_reg)
        if select != None:
            c = mapp[select[0]][select[1]]
            try:
                self.select_sprite.image = c.sprite.image
                self.card_label.text = """
                %s
                Health: %s
                Attack: %s
                Crit: %s
                Price: %s""" % (c.name,c.health,c.attack,c.crit_chance,c.price)
            except: pass
        else: self.select_sprite.image = pyglet.image.load('resc/frame2.png'); self.card_label.text = ''

    def draw(self):
        self.mana_label.draw()
        self.select_sprite.draw()
        self.card_label.draw()
