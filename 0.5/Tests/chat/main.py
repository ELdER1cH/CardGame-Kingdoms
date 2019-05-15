import pyglet
import window_chat_extension
import chat_dependencies.main_chat as main_chat
import chat_dependencies.chat as chat

class Window(main_chat.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.sprite = pyglet.sprite.Sprite(pyglet.image.load("palatin.png"),0,0)

  def on_draw(self):
    super().on_draw()
    self.sprite.draw()
    self.chat_model.draw()
    #self.chat_batch.draw()

  def on_cmd(self,cmd):
    if cmd == '/hello world':
      self.g_print('§cHello, dear fella!')
    else: self.g_print("§cunknown command. '%s'" % (cmd))
          

if __name__ == "__main__":
  window = Window(400,400)
  pyglet.app.run()
