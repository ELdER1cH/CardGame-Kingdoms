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
    
    self.CORDS = {'cords': (0,0)}

  def state_event(self):
    info = {'type': 'cords', **self.CORDS, 'lobby':self.lobby}
    print(">> send", info)
    return json.dumps(info)

  def send(self):
    self.s.sendall(self.state_event().encode())

