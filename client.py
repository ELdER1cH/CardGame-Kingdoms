import socket
import json
  
class Client():
  def __init__(self,ip,port):
    self.s = socket.socket()
    self.s.connect((ip,port))
    self.opponent_found = False
    
    print('<> conncetion established!')

  def send(self,info):
    msg = json.dumps(info)
    self.s.sendall((msg+"\n").encode())

  def send_lobby(self):
    info = {'type': 'lobbyprecaution','lobby': self.lobby}
    return info

  def send_ready(self,ready_state):
    info = {'type': 'ready', 'ready':ready_state}
    return info

  def send_replace_event(self,cardname,pos):
    info = {'type': 'replace', 'replace':(cardname,pos)}
    return info

  def send_swap_event(self,pos1,pos2):
    info = {'type': 'swap', 'swap':(pos1,pos2)}
    return info

  def send_attack_event(self,pos1,pos2):
    info = {'type': 'attack', 'attack':(pos1,pos2)}
    return info

  def send_splash_attack_event(self,pos1,dmg):
    info = {'type': 'splash_attack', 'attack':(pos1,dmg)}
    return info
  
  def send_splash_heal_event(self,pos1,heal_amount):
    info = {'type': 'splash_heal', 'target':(pos1,heal_amount)}
    return info

  def send_move_done(self):
    info = {'type': 'move_done'}
    return info

  def send_chat_message(self,msg):
    info = {'type': 'chat_message', 'msg':msg}
    return info
