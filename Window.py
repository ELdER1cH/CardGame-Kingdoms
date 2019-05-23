class Window(main_chat.Window):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.batch = Batch.CardBatch()
    self.pop_up = pop_up.Pop_Up()

    self.pre_resize_dims = (self.width,self.height)
    self.scale_x = 1
    self.scale_y = 1
        
    pyglet.clock.schedule(self.update)
    

  def update(self,dt):
    self.pop_up.update(dt)
  
  def select(self,target,clicked_card):
    if target.special_tag != "immovable" or target.y == 0:
      if target.owner == self.batch.castle.owner:
        self.batch.select_card(target)
      else:
        self.pop_up.new_red_frame(target.position)
    else:
      self.pop_up.new_red_frame(target.position)

  def on_mouse_press(self,x,y,button,MOD):
    x /= self.scale_x
    y /= self.scale_y
    ###LEFT
    if button == mouse.LEFT:
      
      ###NEW CLICK/ TARGET
      target = self.batch.get_card((x,y))
      if target == None: return
      ###OLD CLICK/ SELECT
      clicked_card = self.batch.get_card(self.batch.select_frame.position)
      #MAKE SURE THERES A CARD AT THE OLD CLICK - IF THERES NONE, TARGET = NEW SELECT
      if clicked_card != None:
        ###HIDE IF DOUBLE CLICK
        if target == clicked_card:
          self.batch.hide(self.batch.select_frame)
          
        #---HAND---
        ###IF SELECT IN HAND  
        elif clicked_card.y == 0:
          ###IF TARGET NOT IN HAND
          if target.y > 0:
            ###IF TARGET IS MINE
            if target.owner == clicked_card.owner:
              ###IF TARGET IS EMPTY FIELD
              if target.special_tag == "unoccupied_field":
                #IF PLAYER HAS ENOUGH MONEY
                if self.batch.castle.mana >= clicked_card.price:
                  self.batch.castle.mana -= clicked_card.price
                  #EMPTY FIELD AND CARD IN HAND SWAP POSITIONS
                  #HAND BEFORE: - if first card were to be placed
                  #C C C C C -> after: E C C C C
                  clicked_card.swap(target,target.position,activate=True)
                  #in Hand: (E=empty field,C=Card in Hand) - (if first card was placed)
                  #E C C C C-> C E C C C-> C C E C C-> C C C E C-> C C C C E-> C C C C C
                  self.batch.update_hand(target)
                  self.batch.hide(self.batch.select_frame)
                  #UPDATE STATS DISPLAY TO SHOW RIGHT MANA AMOUT
                  self.batch.update_disp(clicked_card)
                else:
                  self.pop_up.new_pop_up((x,y),0.5,'TOO COSTLY: %s' % (clicked_card.price))
                  self.pop_up.new_red_frame(clicked_card.position)
              else:
                ###IF NEW CLICK NOT A EMPTY FIELD (AND MY CARD), SELECT THAT CARD
                self.select(target,clicked_card)
            else:
              ###IF TARGET IS NOT MY CARD SHOW A RED FRAME
              self.pop_up.new_red_frame(clicked_card.position)
          else:
            ###IF CARD IS IN HAND SELECT THAT CARD INSTEAD
            self.batch.select_card(target)

        #---NOT HAND---
        else:
          #GET UP, DOWN, LEFT, RIGHT TO SELECT
          adjacent = self.batch.get_adjacent(clicked_card.position)
          for in_reach in adjacent:
            ###IF NEW CARD/ TARGET IS IN REACH OF SELECT
            if target == in_reach:
              ###IF CARD IN REACH IS MY CARD
              if clicked_card.owner == target.owner:
                ##IF CARD IS NOT IMMOVABLE
                if target.special_tag != "immovable":
                  #SWAP POSITION WITH THAT CARD IN REACH
                  clicked_card.swap(target,target.position)
                  #MAKE SURE THE STATS DISPLAY STILL DISPLAYS THE RIGHT CARD - THEY SWAPPED, STATS WOULD DISPLAY YELLOW
                  self.batch.update_disp(clicked_card)
                else:
                  #IF CARD IN REACH == IMMOVABLE, SHOW RED FRAME
                  self.pop_up.new_red_frame(clicked_card.position)
              else:
                #IF CARD IN RANGE IS NOT MY CARD
                clicked_card.fight(target,self.pop_up)
              ##IF TARGET WAS IN REACH, HIDE SELECT, SINCE THERE WAS A SWAO or FIGHT
              self.batch.hide(self.batch.select_frame)
              break
          else:
            ###IF CARD NOT IN REACH, TRY SELECTING THAT CARD
            self.select(target,clicked_card)

      ##SINCE THERES NO SELECTED CARD, TARGET = NEW SELECT
      elif target.special_tag != "unoccupied_field":
        #IF TARGET IS NO EMPTY FIELD, SHOW ITS STATS IN STATS DISPLAY
        ##ONLY DO THIS IF TARGET IS NOT IN ENEMY HAND
        if target.y > 0 and target.y < 800:
          self.batch.disp.update_to_enemy(target)
        #TRY SELECTING THAT CARD
        self.select(target,clicked_card)
      else:
        #IF TARGET IS EMPTY FIELD SHOW RED FRAME
        self.pop_up.new_red_frame(target.position)    
