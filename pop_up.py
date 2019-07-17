import pyglet

class Pop_Up:
    def __init__(self):
        self.pop_ups = []
        
    def your_turn_pop_up(self,delay,pos=(0,0)):
        self.pop_up_label = pyglet.text.Label('<< your turn!',
                                              font_name ='Arial',
                                              font_size=30,
                                              bold=True,
                                              x=pos[0], y=pos[1],
                                              anchor_x='center', anchor_y='center',color=(50,255,50,255))
        self.life_time = 0.8
        self.pop_ups.append([self.pop_up_label,self.life_time])


    def emptyfield_special(self,pos=(0,0),amount=1):
        self.pop_up_label = pyglet.text.Label('+1',
                                              font_name ='Times New Roman',
                                              font_size=20,
                                              bold=True,
                                              x=pos[0]+135//2, y=pos[1]+135//2,
                                              anchor_x='center', anchor_y='center',color=(41, 107, 214,255))
        if amount != 1:
            self.pop_up_label.text = '+' + str(amount)
        self.life_time = 1
        self.pop_ups.append([self.pop_up_label,self.life_time])
    
    def healer_special(self,pos=(),amount=1200):
        self.pop_up_label = pyglet.text.Label("+"+str(amount),
                                              font_name ='Times New Roman',
                                              font_size=20,
                                              bold=True,
                                              x=pos[0]+135//2, y=pos[1]+135//2,
                                              anchor_x='center', anchor_y='center',color=(6, 194, 0,255))
        self.life_time = 1
        self.pop_ups.append([self.pop_up_label,self.life_time])
    
    def new_pop_up(self,pos,life_span=0.3,text='', font_size =12,color=(255,50,50,255),delay=None):
        self.pop_up_label = pyglet.text.Label(text,
                          font_name='Arial',
                          font_size=font_size,
                          bold=True,
                          x=pos[0], y=pos[1],
                          anchor_x='left', anchor_y='center',color=color)
        self.life_time = life_span
        self.pop_ups.append([self.pop_up_label,self.life_time])

    def new_red_frame(self,pos,life_span=0.3):
        self.red_frame = pyglet.sprite.Sprite(pyglet.image.load('resc/red_frame.png'),
                                              pos[0],pos[1])
        self.life_time = life_span
        self.pop_ups.append([self.red_frame,self.life_time])

    def update(self,dt):
        for pops in self.pop_ups:
            if type(pops[0]) == pyglet.text.Label:
                if pops[0].font_name == 'Times New Roman':  
                    pops[0].font_size += 1
                    pops[0].color= (pops[0].color[0],pops[0].color[1],pops[0].color[2],pops[0].color[3] -20)
                    pops[0].y += 2
                    if pops[0].color[3] <= 0:
                        self.pop_ups.remove(pops)
            pops[1] += -dt
            if pops[1] <= 0:
                self.pop_ups.remove(pops)  

    def draw(self):
        for pops in self.pop_ups:
            pops[0].draw()