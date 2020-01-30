import pyglet, socket, sys, json, datetime, threading, time

# '*' = Serverlog; '<>'/'<!>' = GameServerlog

#!!!! how do I measure server load/ max thread load or something
#perhaps just add max open thread threshold for safety.. dunno, test with programm..

HOST = ''
PORT = 6789
loop = True
#cmd_loop = True

def log(info, prefix="",p=True):
    lenght = 30; current_time = prefix + str(datetime.datetime.now())
    with open("serverlog.txt","a") as f:
        text = f'{current_time:<{lenght}}' + "- " + info + "\n"
        f.write(text)
        if p: print(text[:-1])

class Server():
    def __init__(self):
        self.init_socket()
        self.bind()

    def init_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log("Socket successfully created!", "*")
        except socket.error as err:
            log("socket creation failed with error %s" %(err), "*")
            self.close()
        
    def close(self,shut_down=True):
        global loop
        try:
            self.socket.close()
            if shut_down: 
                loop = False
            log("Socket successfully closed!\n--------\n","*")
        except socket.error as e:
            log(str(e),"*")
            log("trying to exit...","*")
            exit()

    
    def bind(self,host=HOST,port=PORT):
        try:
            self.socket.bind((host, port))
            log("Socket successfully bound to address: %s:%s" %(HOST,PORT),"*")
        except socket.error as e:
            log(str(e),"*")
            self.close()
            return
        self.socket.listen()
        log("Socket is listening...","*")

    def restart(self):
        log("Initialising restart...","*")
        self.close(shut_down=False)
        self.init_socket()
        self.bind()
        #self.reconnect() #try reconnecting to all old connections/ users(?)
        log("Restart successfull!","*")

    def glist(self): #show all connections
        log("glist!")

    def qlog(self,logs=10,filter=None): #filter: errors, received, send - show the log or sth..., unnecessary tho, I'm printing it now anyways, soo.. actually only the cmds
                                        #maybe only log the connection feed or so, not my command stuff
        log("qlog!")

    def cmd(self,inp):
        split = inp.split(" ")
        if split[0] == "/close" or split[0] == "/c":
            self.close()
        elif split[0] == "/bind" or split[0] == "/b": #enable parsing arguments to this cmd/ func
            self.bind()
        elif split[0] == "/restart" or split[0] == "/r": #enable parsing arguments to this cmd/ func
            self.restart()
        else: print("unknown cmd!")

class GameServer(Server):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.threads = []
        self.lobbys = {} # lobby#1 : [0,1]
        self.full_lobbys = {} # 0 : [conn1,conn2]
        self.empty_lobbys = {} # 0 : [conn1]
        self.lobby_counter = 0
        self.to_unregister = []

        self.max_lobby_size = 2

        self.shutting_off = False; self.shutt_down_time = 30

        #threading.Thread(target=self.unregister_thread).start()

    def shut_off_timer(self):
        while self.shutting_off:
            time.sleep(1)
            self.shutt_down_time -= 1
            if self.shutt_down_time <= 0:
                self.shutting_off = False
                self.close(shut_down=True)

    def assign_lobby(self,conn):
        #elp = len(self.empty_lobbys); elp2 = []; elp3 = []; flp = len(self.full_lobbys)

        if len(self.empty_lobbys) != 0:
            self.empty_lobbys[0].append(conn)#;elp2 = len(self.empty_lobbys[0])

            if len(self.empty_lobbys[0]) >= self.max_lobby_size:
                l = self.lobby_counter #len(self.full_lobbys)
                for c in self.empty_lobbys[0]:
                    c["lobby"] = l
                self.full_lobbys[l] = self.empty_lobbys.pop(0)#;flp = len(self.full_lobbys)
                log(f"L  popped {self.full_lobbys[conn['lobby']][0]['addr']} & {self.full_lobbys[conn['lobby']][1]['addr']} into lobby {conn['lobby']}","<>")
                info = {'type': 'join'}
                self.notify_lobby(info,conn,True)
                self.lobby_counter += 1
        else:
            if conn in self.connections:
                self.empty_lobbys[0] = [conn]
                conn["lobby"] = None
        #elp3 = len(self.empty_lobbys)
        lis = []
        for c in self.connections:
            lis.append(c["lobby"])
        log(f"L  assigned lobby {conn['lobby']} to {conn['addr']}; full: {len(self.full_lobbys)}, empty: {len(self.empty_lobbys)}; lobbys: {lis}","<>") #"elp:{elp}, elp2:{elp2}, elp3:{elp3}, flp:{flp}""
    
    def register(self,conn):
        #asign lobby to new conn
        if self.shutting_off: self.shutting_off = False

        self.connections.append(conn)
        log(f'>> New connetion from addr: {conn["addr"]} num_conns: {len(self.connections)}',"<>")

        self.assign_lobby(conn)

    def unregister(self,conn):
        self.connections.remove(conn)
        log(f'<< connection lost: {conn["addr"]}, lobby: {conn["lobby"]}, num_conns: {len(self.connections)}',"<>")
        if conn["lobby"] != None:
            #send remaining lobby message to leave/ end current game!!! -> implement in main.py!!!
            info = {'type': 'abort'}
            self.notify_lobby(info,conn)

            if conn["lobby"] in self.full_lobbys.keys():
                self.full_lobbys[conn["lobby"]].remove(conn)
                self.assign_lobby(self.full_lobbys.pop(conn["lobby"])[0])
        else: 
            self.empty_lobbys[0].remove(conn)
        log(f'L  updated lobbys. full: {len(self.full_lobbys)}, empty: {len(self.empty_lobbys)}',"<>")

        del conn

        if len(self.connections) <= 0:
            if not self.shutting_off:
                self.shutting_off = True; self.shutt_down_time = 30
                threading.Thread(target=self.shut_off_timer).start()
                log("! Starting shutt off timer! t: -30s","*")

    def notify_lobby(self,data,conn,send_sender=False):
        if len(self.full_lobbys[conn["lobby"]]) >= 2:
            for c in self.full_lobbys[conn["lobby"]]:
                if send_sender or c != conn:
                    try:
                        c["conn"].sendall((json.dumps(data) + "\n").encode())
                    except:
                        log(f"failed to send data: {data} to {c['addr']}; lobby {c['lobby']}","<>")
            log(f"S>  send {data} lobby: {conn['lobby']}","<>")    

    def unregister_thread(self):
        while loop:
            while len(self.to_unregister) > 0:
                self.unregister(self.to_unregister.pop(0))

    def linesplit(self,conn,bits=1096):
        while loop:
            try:
                buffer = conn["conn"].recv(bits).decode()
                if not buffer:
                    return
            except:
                break  
            buffering = True
            while buffering:
                if "\n" in buffer:
                    (message, buffer) = buffer.split("\n", 1)
                    yield message
                else:
                    try:
                        more = conn["conn"].recv(bits).decode()#
                        if not more:
                            return
                    except:
                        break  
                    if not more:
                        buffering = False
                    else:
                        buffer += more
            if buffer:
                yield buffer
        
        self.unregister(conn)
        #self.to_unregister.append(conn)

    def connection_loop(self,conn):
                ls = self.linesplit(conn)
                for message in ls:
                    data = json.loads(message)
                    log(f"G<  got {data} from {conn['addr']}","<>")
                    self.notify_lobby(data,conn)

    def main_loop(self):
        log("! main loop active!", "<>")
        while loop:
            try:
                conn, addr = self.socket.accept()
            except: #potential shutdown point, if I want to.
                log(f"! error whilst establishing a connection! shutting down... (open threads: {threading.active_count()})","<!>")

                #self.restart()
                #log(f"open threads: {threading.active_count()}","<>")
                #return
                break

            new_conn = {"conn" : conn, "addr" : addr, "lobby" : None}
            self.register(new_conn)        
            self.threads.append(threading.Thread(target=self.connection_loop,args=([new_conn])).start())
        
        log("! main loop terminated!", "<>")

if __name__ == "__main__":
    server = GameServer()
    server.main_loop()
    # while cmd_loop:
    #     inp = input(">")
    #     server.cmd(inp)
