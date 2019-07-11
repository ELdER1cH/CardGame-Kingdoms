import socket
import json
import threading

HOST = ''  # Standard loopback interface address (localhost)
PORT = 6789        # Port to listen on (non-privileged ports are > 1023)

USERS = set()
LOBBIES = {1:[]}
LOBBY_SIZE = 2
run = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Enter Host:')
userhost = input()

HOST = userhost

try:
    s.bind((HOST, PORT))
except socket.error as e:
    print(e)
    
print('<> server bound to addr: %s:%s' % (HOST,PORT))

s.listen()

def lobby_change(lobby,lobbysize):
    info = {'type': 'lobby', 'lobby': lobby, 'lobbysize': lobbysize}
    print(">> send", info)
    return json.dumps(info)

def new_message(t,tval=None):
    if tval == None:
        info = {'type':t}
    else:
        info = {'type':t,t:tval}
    print(">> send", info)
    return info

def user_count():
    info = {'type': 'users', 'users': len(USERS)}
    print(">> send", info)
    return json.dumps(info)

def notify_users(message):
    if USERS:
        for user in USERS:
            user.sendall(message.encode())
    else:
        global run
        run = False
        s.close()

def notify_lobby(data,lobby,conn=None):
    lob = LOBBIES[lobby]
    for user in lob:
        if user != conn:
            user.sendall(json.dumps(data).encode())               

def unregister(conn,addr,lobby):
    print(f'<< connection lost: {addr} lobby: {lobby}')
    USERS.remove(conn)
    LOBBIES[lobby].remove(conn)

    top_lobby = len(LOBBIES)
    
    if lobby != top_lobby:
        users_to_add = set()
        for user in LOBBIES[lobby]:
            users_to_add.add(user)
            
        while users_to_add:
            if len(LOBBIES[top_lobby]) == LOBBY_SIZE:
                top_lobby += 1
                LOBBIES[top_lobby] = []
                print(f"<> new lobby: {top_lobby}")
            user = users_to_add.pop()
            LOBBIES[top_lobby] += [user]
            LOBBIES[lobby].remove(user)
            print(f"<> changed user lobby from lobby {lobby} to {top_lobby}")

    lobbysize = len(LOBBIES[lobby])
    info = {'type': 'lobby', 'lobby': lobby, 'lobbysize': lobbysize}
    print(">> send", info)
    notify_lobby(info,lobby)
    
    if not USERS:
        global run
        run = False
        s.close()
        
def connection_loop(conn,addr,lobby):
    while run:
        try:
            data = json.loads(conn.recv(4096).decode())
            if not data:
                return
            #m = json.dumps(data)
            #conn.sendall(m.encode())
            #notify_users(m)
            notify_lobby(data,int(data['lobby']),conn)
            if lobby != int(data['lobby']):
                lobby = int(data['lobby'])
        except:
            break
    unregister(conn,addr,lobby)        
        
def register(conn,addr):
    print(f'<< New connetion from addr: {addr}')

    lobby = len(LOBBIES)
    if len(LOBBIES[lobby]) == LOBBY_SIZE:
        lobby += 1
        LOBBIES[lobby] = []
        print(f"<> new lobby: {lobby}")
    
    LOBBIES[lobby] += [conn]
    lobbysize = len(LOBBIES[lobby])

    info = {'type': 'lobby', 'lobby': lobby, 'lobbysize': lobbysize}
    print(">> send", info)
    notify_lobby(info,lobby)
    
    USERS.add(conn)
    return lobby

while run:
    print('<> awaiting connection')
    try:
        conn, addr = s.accept()
    except:
        print("<> server shut down!")
        break
    lobby = register(conn,addr)        
    threading.Thread(target=connection_loop,args=(conn,addr,lobby)).start()