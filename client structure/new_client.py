import socket
import json
  
class Client():
  def __init__(self,ip,port):
    self.s = socket.socket()
    self.s.connect((ip,port))

    #get rid of all this messages received at the end! have only one!
    
    print('<> conncetion established!')
    
    self.s.sendall(socket.gethostname().encode())
    self.lobby = int(self.s.recv(1024).decode())
    print(f"<< my lobby: {self.lobby}")
    #self.lobbysize = int(self.s.recv(1024).decode())
    #print(f"<< my lobby size: {self.lobbysize}")

  def send(self,info):
    #print(">> send", info)
    self.s.sendall(info.encode())

  def send_lobby(self):
    info = {'type': 'lobbyprecaution','lobby': self.lobby}
    self.send(json.dumps(info))

  def send_ready(self,ready_state):
    info = {'type': 'ready', 'ready':ready_state,'lobby': self.lobby}
    self.send(json.dumps(info))

  def send_replace_event(self,cardnum,pos):
    info = {'type': 'replace', 'replace':(cardnum,pos), 'lobby':self.lobby}
    self.send(json.dumps(info))

  def send_swap_event(self,pos1,pos2):
    info = {'type': 'swap', 'swap':(pos1,pos2), 'lobby':self.lobby}
    self.send(json.dumps(info))

  def send_attack_event(self,pos1,pos2):
    info = {'type': 'attack', 'attack':(pos1,pos2), 'lobby':self.lobby}
    self.send(json.dumps(info))

