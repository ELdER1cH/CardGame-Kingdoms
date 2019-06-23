import socket
import json
  
class Client():
  def __init__(self,ip,port):
    self.s = socket.socket()

    self.s.connect((ip,port))
    print('<> conncetion established!')
    
    self.s.sendall(socket.gethostname().encode())
    self.lobby = int(self.s.recv(1024).decode())
    print(f"<< my lobby: {self.lobby}")
    self.lobbysize = int(self.s.recv(1024).decode())
    print(f"<< my lobby size: {self.lobbysize}")
    
    self.CORDS = {'cords': (0,0)}

  def state_event(self,x,y,button):
    info = {'type': 'press', 'press':(x,y,button), 'lobby':self.lobby}
    print(">> send", info)
    return json.dumps(info)

  def send(self,x,y,button):
    self.s.sendall(self.state_event(x,y,button).encode())

