import pyglet
import copy
import Cards

class Stats_Display():
    def __init__(self):
        #self.document = pyglet.text.document.FormattedDocument('This is a multi line document. This is a multi line document.')
        #self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255)))
        #self.text = pyglet.text.layout.TextLayout(self.document,240,420,multiline=True)
        self.blank = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/blank_card.png"),135*6, 10)
        self.select_sprite = pyglet.sprite.Sprite(pyglet.image.load("resc/gray_frame.png"),self.blank.x+50, self.blank.y+220)
        self.mana_label = pyglet.text.Label("",
                          font_name='Times New Roman',
                          font_size=12,
                          bold=True,color=(109, 43, 43,255),
                          x=720, y=790,
                          anchor_x='center', anchor_y='top',multiline=True,width=220)
    # ---------------------------Card Describtion ----------------------------------------
        self.card_describtion_card = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            color=(109, 43, 43,255),
                            x=self.blank.x+50, y=self.blank.y+160,
                            anchor_x='left', anchor_y='top',multiline=True,width=265)
    # ------------------------- Card Name ----------------------------------------------------    
        self.card_name = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=24,
                            bold=True,color=(109, 43, 43,255),
                            x=self.blank.x+self.blank.width//2, y=self.blank.y+500,
                            anchor_x='center', anchor_y='center')
        
    # -------------------------- Stats Block ------------------------------------------------------------        
        self.card_damage = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            bold = True,color=(109, 43, 43,255),
                            x=self.blank.x+85, y=self.blank.y+205,
                            anchor_x='left', anchor_y='top')
        self.card_health = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            bold = True,color=(109, 43, 43,255),
                            x=self.blank.x+200, y=self.blank.y+205,
                            anchor_x='left', anchor_y='top')
        self.card_cost = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            bold = True,color=(109, 43, 43,255),
                            x=self.blank.x+300, y=self.blank.y+205,
                            anchor_x='left', anchor_y='top')
    
        

    def update(self,mana,max_mana,mana_reg,target):
        self.mana_label.text = """
        Mana: %s
        Max Mana: %s
        Mana Reg: %s""" % (mana,max_mana,mana_reg)
        try:
            self.select_sprite.image = pyglet.image.load(target.img[:-4]+"_large.png")
        except:
            self.select_sprite.image = pyglet.image.load(target.img)
        

        self.card_describtion_card.text = target.description
        self.card_name.text = target.name
        self.card_damage.text = str(target.dmg)
        self.card_health.text = str(target.health)
        self.card_cost.text = str(target.price)
        
        
        
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
        self.blank.draw()
        self.select_sprite.draw()
        
        self.card_describtion_card.draw()
        self.card_name.draw()
        self.card_damage.draw()
        self.card_health.draw()
        self.card_cost.draw()