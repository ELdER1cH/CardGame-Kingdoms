import pyglet
import copy

class Stats_Display():
    def __init__(self):
        #self.document = pyglet.text.document.FormattedDocument('This is a multi line document. This is a multi line document.')
        #self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255)))
        #self.text = pyglet.text.layout.TextLayout(self.document,240,420,multiline=True)
        self.select_sprite = pyglet.sprite.Sprite(pyglet.image.load('resc/gray_frame.png'),660, 600)
        self.mana_label = pyglet.text.Label("",
                          font_name='Times New Roman',
                          font_size=12,
                          bold=True,color=(109, 43, 43,255),
                          x=720, y=790,
                          anchor_x='center', anchor_y='top',multiline=True,width=220)
        self.card_label = pyglet.text.Label("",
                          font_name='Times New Roman',
                          font_size=12,
                          bold=True,color=(109, 43, 43,255),
                          x=720, y=600,
                          anchor_x='center', anchor_y='top',multiline=True,width=180)
        

    def update(self,mana,max_mana,mana_reg,target):
        self.mana_label.text = """
        Mana: %s
        Max Mana: %s
        Mana Reg: %s""" % (mana,max_mana,mana_reg)

        self.select_sprite.image = pyglet.image.load(target.img)
        self.card_label.text = """
        %s
        Health: %s
        Attack: %s
        Crit: %s
        Price: %s""" % (target.name,target.health,target.dmg,
                        target.crit,target.price)
        
    def clear(self):
        self.mana_label.text = ""
        self.select_sprite.image = pyglet.image.load('resc/gray_frame.png')
        self.card_label.text = ""
        
    def update_to_enemy(self,target):
        self.select_sprite.image = pyglet.image.load(target.img)
        self.card_label.text = """
        %s
        Health: %s
        Attack: %s
        Crit: %s
        Price: %s""" % (target.name,target.health,target.dmg,
                        target.crit,target.price)

    def draw(self):
        self.mana_label.draw()
        self.select_sprite.draw()
        self.card_label.draw()