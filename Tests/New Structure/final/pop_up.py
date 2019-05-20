import pyglet

class Pop_Up:
    def __init__(self):
        self.pop_ups = []

    def new_pop_up(self,pos,life_span=0.3,text=''):
        self.pop_up_label = pyglet.text.Label(text,
                          font_name='Arial',
                          font_size=12,
                          bold=True,
                          x=pos[0], y=pos[1],
                          anchor_x='left', anchor_y='center',color=(255,50,50,255))
        self.life_time = life_span
        self.pop_ups.append([self.pop_up_label,self.life_time])

    def new_red_frame(self,pos,life_span=0.3):
        self.red_frame = pyglet.sprite.Sprite(pyglet.image.load('resc/red_frame.png'),
                                              pos[0],pos[1])
        self.life_time = life_span
        self.pop_ups.append([self.red_frame,self.life_time])

    def update(self,dt):
        for pops in self.pop_ups:
            pops[1] += -dt
            if pops[1] <= 0:
                self.pop_ups.remove(pops)  

    def draw(self):
        for pops in self.pop_ups:
            pops[0].draw()

    
