import socket
import json
  
class Client():
  def __init__(self,ip,port):
    self.s = socket.socket()
    self.s.connect((ip,port))
    
    print('<> conncetion established!')

  def send(self,info):
    #print(">> send", info)
    self.s.sendall(info.encode())

  def send_lobby(self):
    info = {'type': 'lobbyprecaution','lobby': self.lobby}
    self.send(json.dumps(info))

  def send_ready(self,ready_state):
    info = {'type': 'ready', 'ready':ready_state,'lobby': self.lobby}
    self.send(json.dumps(info))

  def send_replace_event(self,cardname,pos):
    info = {'type': 'replace', 'replace':(cardname,pos), 'lobby':self.lobby}
    self.send(json.dumps(info))

  def send_swap_event(self,pos1,pos2):
    info = {'type': 'swap', 'swap':(pos1,pos2), 'lobby':self.lobby}
    self.send(json.dumps(info))

  def send_attack_event(self,pos1,pos2):
    info = {'type': 'attack', 'attack':(pos1,pos2), 'lobby':self.lobby}
    self.send(json.dumps(info))

  def send_move_done(self):
    info = {'type': 'move_done', 'lobby':self.lobby}
    self.send(json.dumps(info))