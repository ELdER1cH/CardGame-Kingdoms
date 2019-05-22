try:
  import pyglet
  from pyglet.gl import *
  from pyglet.window import key,mouse
  import chat_dependencies.chat as chat
  import chat_dependencies.text_input as ti
  #import win32clipboard
except ImportError as err:
  print("couldn't load modue. %s" % (err))

#command input
#variety of textures displayed simultanuously
#simple player movement
#menu
#inventory
#items?
#simple bot
#ressources and environment interaction (destroying and boundries for player)
#procedual generated/ predefinded map with finite texture locations

class Model(object):
  def __init__(self,batch):
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    self.batch = batch
    self.command_input_widget = pyglet.graphics.Batch()
    self.command_input_widget_state = False
    self.new_input_widget('',3,3,500,self.command_input_widget)
    self.chat = chat.Chat(3,(12+self.ciw.height),500,15)
    
  def load_textures(self):
    pass
  
  def update(self,dt):
    pass
    
  def draw(self):
    if self.command_input_widget_state == True:
      self.command_input_widget.draw()
      self.chat.draw()
    self.batch.draw()
  
  def new_input_widget(self,text,x,y,width,batch):
    self.ciw = ti.TextWidget(text, x, y, width, batch)

  
class Window(pyglet.window.Window): 
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.set_location(200, 100)
    pyglet.clock.schedule(self.update)
    self.keys = pyglet.window.key.KeyStateHandler()
    self.push_handlers(self.keys)
    self.chat_batch = pyglet.graphics.Batch()
    self.version = pyglet.text.Label('main chat',y=2,
                                     x=self.width-1,font_name='Times New Roman',
                                     anchor_x='right',batch=self.chat_batch)
    self.chat_model = Model(self.chat_batch)
    self.focus = None
    self.g_print = self.chat_model.chat.g_print
    
  def update(self,dt):
    self.version.x = self.width-2
    self.chat_model.update(dt)
  
  def on_key_press(self,KEY,MOD):
    if not self.chat_model.command_input_widget_state:
      if KEY == key.T:
        self.chat_model.command_input_widget_state = not self.chat_model.command_input_widget_state
        self.set_focus(self.chat_model.ciw)
        self.chat_model.ciw.document.text = '/clear_prompt -n *'
      ##game movement 
    else:
      if KEY == key.ESCAPE: self.chat_model.command_input_widget_state = False
      if KEY == key.ENTER:
        if len(self.chat_model.ciw.document.text) > 0:
          if self.chat_model.ciw.document.text[0] == '/':
            split = self.chat_model.ciw.document.text.split(" ")
            self.on_cmd(split)
          else:
            self.g_print(self.chat_model.ciw.document.text)
            self.chat_model.ciw.document.text = ''
        self.chat_model.command_input_widget_state = False
        self.chat_model.chat.update()

  def on_cmd(self,cmd):
    pass

  def on_draw(self):
    pass
    #self.clear()
    #self.chat_model.draw()
    #self.batch.draw()

  def on_text(self, text):
    if self.focus and self.chat_model.ciw.document.text != '/clear_prompt -n *':
      if len(self.chat_model.ciw.document.text) <= 50:
        self.focus.caret.on_text(text)
      else: self.g_print("§cno more than 50 letters allowed."); self.chat_model.chat.update()
    else: self.chat_model.ciw.document.text = ''
    
  def on_text_motion(self, motion):
    if self.focus:
      self.focus.caret.on_text_motion(motion)
      
  def on_text_motion_select(self, motion):
    if self.focus:
      self.focus.caret.on_text_motion_select(motion)

  def set_focus(self, focus):
    if self.focus:
      self.focus.caret.visible = False
      self.focus.caret.mark = self.focus.caret.position = 0
    self.focus = focus
    if self.focus:
      self.focus.caret.visible = True
      self.focus.caret.mark = 0
      self.focus.caret.position = len(self.focus.document.text)

if __name__ == '__main__':
  window = Window()
  glClearColor(0.1,0.1,0.1,1)
  pyglet.app.run()
  
