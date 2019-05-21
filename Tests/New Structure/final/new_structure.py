import pyglet
from pyglet.gl import *
import pop_up, Batch, Cards, Card
from pyglet.window import key, mouse
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

INDENTATION_RIGHT = 2

class Window(pyglet.window.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.batch = Batch.CardBatch()
    self.pop_up = pop_up.Pop_Up()
    
    pyglet.clock.schedule(self.update)

  def update(self,dt):
    self.pop_up.update(dt)

  def on_mouse_press(self,x,y,button,MOD):
    #left click?
    if button == mouse.LEFT:
      target = self.batch.get_card((x,y))
      #clicked on a card?
      if target != None:
        selected_card = self.batch.get_card(self.batch.select_frame.position)
        #is there already an selected card?
        if selected_card != None:
          if target.owner == self.batch.castle.owner:
            if selected_card != target:
              adjacent = self.batch.get_adjacent(selected_card.position)
              for allowed_card in adjacent:
                #if clicked card adjacent to selected_card
                if target == allowed_card:
                    #now stuff could happen - attack, move, etc.

                    #move if own field
                    p = target.position
                    target.position = selected_card.position
                    selected_card.position = p
                    self.batch.hide(self.batch.select_frame) 
                    return
              self.pop_up.new_red_frame(selected_card.position)
            else:
              #undo selected_card
              self.batch.hide(self.batch.select_frame)
              
          else:
            #indicate error with red_frame
            self.pop_up.new_red_frame(selected_card.position)   
          
        #set selected_card if own card and not immovable
        elif target.owner == self.batch.castle.owner:
          if target.special_tag != "immovable":
            self.batch.select_card(target) 
            #target.replace(Cards.gray,owner="gray")
          else:
            self.pop_up.new_red_frame(target.position)
        else:
            self.pop_up.new_red_frame(target.position)

  def on_key_press(self,KEY,MOD):
    if KEY == key.S:
      self.batch.swap()
      print(self.batch.castle.mana)
          
  def on_draw(self):
    self.clear()
    self.batch.draw()
    self.pop_up.draw()
    fps_display.draw()

if __name__ == "__main__":
  width = 600+120*INDENTATION_RIGHT;height =800
  window = Window(width,height,"New Stucture Testing",resizable=True,vsync=True)
  glClearColor(255,255,255,255)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  fps_display = pyglet.window.FPSDisplay(window)
  fps_display.label.font_size = 15
  pyglet.app.run()
