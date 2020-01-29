import pyglet

class Window(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super.__init__(*args,**kwargs)

    def on_draw(self):
        pass

if __name__ == "__main__":
    win1 = Window(100,200,"Win1")
    win2 = Window(100,200,"Win2")
    pyglet.app.run()

""" import time
    last = ""
    while True:
        time.sleep(1)
        with open("writenreadtest.txt","r") as f:
            lines =f.readlines()[-1]
            if lines != last:
                last = lines
                print(f"%s" % last[:-1])
"""
