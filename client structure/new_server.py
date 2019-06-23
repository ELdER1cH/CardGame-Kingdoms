import socket
import json
import threading

#td:
#add player ids again


HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 8765        # Port to listen on (non-privileged ports are > 1023)

USERS = set()
LOBBIES = {1:[]}
LOBBY_SIZE = 2
run = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    if USERS:       # asyncio.wait doesn't accept an empty list
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
    notify_users(user_count())
    #notify_lobby(new_message('message',tval='! lobby partner disconnected - trying to find new lobby..'),
    #             lobby)
    #notify_lobby(new_message('message',tval='! lobby partner disconnected .. trying to find new lobby..'),
    #                 lobby)
    #notify_lobby({'! lobby partner disconnected .. trying to find new lobby..'},lobby)

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
    else:
        notify_lobby(new_message('message',tval='! no new lobby found.. wait for new users to join (/leave)'),
                     lobby)
    lobbysize = len(LOBBIES[lobby])
    info = {'type': 'lobby', 'lobby': lobby, 'lobbysize': lobbysize}
    print(">> send", info)
    notify_lobby(info,lobby)
    #if len(lobby) == 2:

    #else:
            #first check if top lobby!
            #delete lobby and put it on top/ to top lobby, we want this to
            #work with lobbies >= 2!
    #        if int(data['lobby']) != len(LOBBIES):
        
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
    hostname = conn.recv(4096).decode()
    print('<< New connetion from addr: %s hostname: %s' % (addr,hostname))

    lobby = len(LOBBIES)
    if len(LOBBIES[lobby]) == LOBBY_SIZE:
        lobby += 1
        LOBBIES[lobby] = []
        print(f"<> new lobby: {lobby}")
    LOBBIES[lobby] += [conn]
    conn.sendall(str(lobby).encode())
    print(f">> send lobby '{lobby}' to hostname:{addr[1]}")
    lobbysize = len(LOBBIES[lobby])
    #conn.sendall(str(lobbysize).encode())
    #print(f">> send lobby size '{len(LOBBIES[lobby])}' to hostname:{addr[1]}")

    info = {'type': 'lobby', 'lobby': lobby, 'lobbysize': lobbysize}
    print(">> send", info)
    notify_lobby(info,lobby)
    
    USERS.add(conn)
    #notify_users(user_count())
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
