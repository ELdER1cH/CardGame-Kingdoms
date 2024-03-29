import pyglet
import copy
import Cards, Batch

width = 1920;height =1080
class Stats_Display():
    def __init__(self):
        #self.document = pyglet.text.document.FormattedDocument('This is a multi line document. This is a multi line document.')
        #self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255)))
        #self.text = pyglet.text.layout.TextLayout(self.document,240,420,multiline=True)
        
    
# --- Left Side -------------------------------------------------------------------
    # --- Rounds Counter ----------------------------------------------------------
        self.rounds_counter_number = pyglet.text.Label("",
                                font_name='Bahnschrift Light', font_size=40,
                                bold = True,color=(0, 0,0,255),
                                x=113, y=70,
                                anchor_x='center', anchor_y='center')
        self.mana_label = pyglet.text.Label("",
                        font_name='Bahnschrift Light',
                        font_size=35,
                        bold=True,color=(0, 0, 0,255),
                        x=430, y=90,
                        anchor_x='center', anchor_y='center')#,multiline=True,width=400

        self.burg_label = pyglet.text.Label("?",
                        font_name='Bahnschrift Light',
                        font_size=28,
                        bold=True,color=(255, 255, 255,255),
                        x=290, y=860,
                        anchor_x='center', anchor_y='center')

# ---Right Side -------------------------------------------------------------------
    # --- Side Card ---------------------------------------------------------------
        self.blank = pyglet.sprite.Sprite(pyglet.image.load("resc/jolas/blank_card.png"),1530, height //4, )
        #anchor_x = 'center', anchor_y = 'center'
        self.select_sprite = pyglet.sprite.Sprite(pyglet.image.load("resc/gray_frame.png"),self.blank.x+50, self.blank.y+220)
        # --- Card Describtion ---
        self.card_describtion_card = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=12,
                            color=(109, 43, 43,255),
                            x=self.blank.x+50, y=self.blank.y+160,
                            anchor_x='left', anchor_y='top',multiline=True,width=265)
        # --- Card Name ---
        self.card_name = pyglet.text.Label("",
                            font_name='Bahnschrift Light', font_size=24,
                            bold=True,color=(109, 43, 43,255),
                            x=self.blank.x+self.blank.width//2, y=self.blank.y+500,
                            anchor_x='center', anchor_y='center')    
        # --- Stats Block ---
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
    
        
#
    def update(self,mana,max_mana,target,round_counter=None):
        self.mana_label.text = "%s/%s" % (mana,max_mana)
        try:
            self.select_sprite.image = pyglet.image.load(target.img[:-4]+"_large.png")
        except:
            self.select_sprite.image = pyglet.image.load(target.img)
        
        # Round Counter
        self.rounds_counter_number.text = str(round_counter) 

        # Side Card    
        self.card_describtion_card.text = target.description
        self.card_name.text = target.name
        self.card_damage.text = str(int(target.dmg))
        self.card_health.text = str(int(target.health))
        self.card_cost.text = str(int(target.price))
        
        
        
    def clear(self):
        self.mana_label.text = ""
        self.select_sprite.image = pyglet.image.load('resc/gray_frame.png')
        
    def update_to_enemy(self,target):
        try:
            self.select_sprite.image = pyglet.image.load(target.img[:-4]+"_large.png")
        except:
            self.select_sprite.image = pyglet.image.load(target.img)

        # Side Card    
        self.card_describtion_card.text = target.description
        self.card_name.text = target.name
        self.card_damage.text = str(int(target.dmg))
        self.card_health.text = str(int(target.health))
        self.card_cost.text = str(int(target.price))

    def draw(self):
        self.mana_label.draw()
        self.blank.draw()
        self.select_sprite.draw()

        self.burg_label.draw()
        
        #Rounds Counter
        self.rounds_counter_number.draw()


        # Side Card
        self.card_describtion_card.draw()
        self.card_name.draw()
        self.card_damage.draw()
        self.card_health.draw()
        self.card_cost.draw()