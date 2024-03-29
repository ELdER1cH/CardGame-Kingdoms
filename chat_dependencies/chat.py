import pyglet

#make everything more readable (blurr behind chat, nicer colours)

class Chat():
  def __init__(self,x,y,width,maxwords):
    self.display = []
    self.mw = maxwords
    self.text_labels = []
    self.batch = pyglet.graphics.Batch()
    height = 20
    for i in range(1,(self.mw+1)):
      text_label = pyglet.text.Label('',y=y+height*(i-1),x=x, 
                                     anchor_x='left',batch=self.batch,
                                     bold=False,
                                     font_size=15, font_name='Calibri_Light')
      self.text_labels.append(text_label)
      
  def g_print(self,text):
    #print(text)#end=','
    self.add_to_chat(text)

  def update(self):
    for tl in range(0,len(self.display)):
      self.text_labels[tl].text = self.display[tl][2:]
      if self.display[tl][0:2] == '§c':
        self.text_labels[tl].color = (255,50,50,220)
      elif self.display[tl][0:2] == '§g':
        self.text_labels[tl].color = (50,200,50,255)
      else:
        self.text_labels[tl].text = self.display[tl]
        self.text_labels[tl].color = (135,0,135,255)
        

  def add_to_chat(self,text):
    if len(self.display) < self.mw:
      self.display.reverse()
      self.display.append(text)
      self.display.reverse()
    else:
      self.display.insert(0,text)
      self.display.reverse()
      self.display.remove(self.display[0])
      self.display.reverse()
    self.update()
    
  def draw(self):
    self.batch.draw()

