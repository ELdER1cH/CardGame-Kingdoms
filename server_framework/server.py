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
    with open("server_framework/serverlog.txt","a") as f:
        text = f'{current_time:<{lenght}}' + ">> " + info + "\n"
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

        self.max_lobby_size = 2

        self.shutting_off = False; self.shutt_down_time = 30

    def shut_off_timer(self):
        while self.shutting_off:
            time.sleep(1)
            self.shutt_down_time -= 1
            if self.shutt_down_time <= 0:
                self.shutting_off = False
                self.close(shut_down=True)
    
    def register(self,conn):
        #asign lobby to new conn
        if self.shutting_off: self.shutting_off = False

        self.connections.append(conn)
        log(f'<< New connetion from addr: {conn["addr"]} num_conns: {len(self.connections)}',"<>")

        elp = self.empty_lobbys.copy(); elp2 = []; elp3 = []; flp = []

        if len(self.empty_lobbys) != 0:
            self.empty_lobbys[0].append(conn);elp2 = self.empty_lobbys.copy()

            if len(self.empty_lobbys[0] >= self.max_lobby_size):
                for c in self.empty_lobbys[0]:
                    c["lobby"] = len(self.full_lobbys)
                self.full_lobbys[len(self.full_lobbys)] = self.empty_lobbys.pop(0);flp = self.full_lobbys.copy()
        else:
            self.empty_lobbys[0] = [conn]
        elp3 = self.empty_lobbys.copy()
        log(f"Assigned lobby {conn['lobby']} to {conn['addr']}; elp:{elp}, elp2{elp2}, elp3{elp3}, flp{flp}","<>")

    def unregister(self,conn):
        self.connections.remove(conn)
        log(f'<< connection lost: {conn["addr"]}, lobby: {conn["lobby"]}, num_conns: {len(self.connections)}',"<>")
        if conn["lobby"] != None:
            self.full_lobbys[conn["lobby"]].remove(conn)
            self.empty_lobbys[0] = self.full_lobbys.pop(conn["lobby"])
            #send remaining lobby message to leave/ end current game!!! -> implement in main.py!!!
            info = {'type': 'abort'}
            self.notify_lobby(info,conn)
        else: 
            self.empty_lobbys[0].remove(conn)
        log(f'updated lobbys. full: {self.full_lobbys}, empty: {self.empty_lobbys}',"<>")

        del conn

        if len(self.connections) <= 0:
            self.shutting_off = True; self.shutt_down_time = 30
            threading.Thread(target=self.shut_off_timer).start()
            log("Starting shutt off timer! t: -30s","<>")

    def notify_lobby(self,data,conn):
        if len(self.full_lobbys[conn["lobby"]]) >= 2:
            for c in self.full_lobbys[conn["lobby"]]:
                if c != conn:
                    c["conn"].sendall(json.dumps(data).encode())
            log(f">>lsend {data} lobby: {self.full_lobbys[conn['lobby']]}","<>")          

    def connection_loop(self,conn):
        while loop:
            try:
                data = json.loads(conn.recv(4096).decode())
                log(f"G << got {data} from {addr}","<>")
                #use operators here! (the yield and stuff thing) to make sure only 'whole' messages are handled!
                if not data:
                    return
                notify_lobby(data,conn)
            except:
                break
        self.unregister(conn)  

    def main_loop(self):
        log("main loop active!", "<>")
        while loop:
            try:
                conn, addr = self.socket.accept()
            except: #potential shutdown point, if I want to.
                log(f"error whilst establishing a connection! shutting down... (open threads: {threading.active_count()})","<!>")

                #self.restart()
                #log(f"open threads: {threading.active_count()}","<>")
                #return
                break

            new_conn = {"conn" : conn, "addr" : addr, "lobby" : None}
            self.register(new_conn)        
            self.threads.append(threading.Thread(target=self.connection_loop,args=([new_conn])).start())

if __name__ == "__main__":
    server = GameServer()
    server.main_loop()
    # while cmd_loop:
    #     inp = input(">")
    #     server.cmd(inp)