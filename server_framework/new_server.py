import socket, sys, json, datetime, threading, time

HOST = ''
PORT = 29428

def log(info, prefix="",p=True): # '*' = Serverlog; '<>'/'<!>' = GameServerlog
    lenght = 30; current_time = prefix + str(datetime.datetime.now())
    with open("serverlog.txt","a") as f:
        text = f'{current_time:<{lenght}}' + " - " + info + "\n"
        f.write(text) #how isn't this causing race conditions? xD -> the file is most certainly accessed by multiple threads at the same time.. somehow it works.. nice :D I think ist because CPythons threading isnt "reaL" threading... xD (someone on stackoverflow said so, didnt dig deeper, I wont complain if it works)
        if p: print(text[:-1])

class Server():
    def __init__(self):
        self.init_socket()
        self.bind()
        self.loop = True
        self._lock = threading.Lock()     

    def init_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log("Socket successfully created!", "*")
        except socket.error as err:
            log("socket creation failed with error %s" %(err), "*")
            self.close()
        
    def close(self):
        try:
            self.socket.close()
            self.loop = False
            log("Socket successfully closed!\n--------\n","*")
        except socket.error as e:
            log(str(e),"*")
            log("trying to exit...","*")
            quit()
    
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

class GameServer(Server):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.lobbys = {} # {lobby_nr : [0,1]}
        self.waiting_for_lobby = None
        self.lobby_counter = 0

        self.shutting_off = False
        self.shut_down_time = 30

    def shut_off_timer(self):
        while self.shutting_off:
            time.sleep(1)
            self.shut_down_time -= 1
            if self.shut_down_time <= 0:
                self.shutting_off = False
                self.close()

    """def close(self):
        try:
            self.loop = False
            for conn in self.connections:
                conn["conn"].close()
            #while threading.active_count() > 3: #2 -> 2 if no inp thread (/loop) (main programm/ programm with out extra active threads consists of two it seems ^^) - shut down threads also counts as one extra!..
            #    pass
            self.socket.close()
            log("Socket successfully closed!\n--------\n","*")
        except socket.error as e:
            log(str(e),"*")
            log("trying to exit...","*")
            exit()"""

    def register(self,conn):
        if self.shutting_off: self.shutting_off = False
        self.connections.append(conn)
        log(f'New connetion from addr: {conn["addr"]} num_conns: {len(self.connections)}',">>>")
        with self._lock:
            self.assign_lobby(conn)

    def unregister(self,conn):
        with self._lock:
            self.connections.remove(conn)
            log(f'Lost connection: {conn["addr"]}, lobby: {conn["lobby"]}, num_conns: {len(self.connections)}',"<<<")
            if conn["lobby"] != None:
                if conn["lobby"] in self.lobbys.keys(): #probably unnecessary.. lobby_mate["lobby"] = None fixed this occuring.. pretty sure.. :)
                    info = {'type': 'abort'}
                    self.notify_lobby(info,conn)                
                    self.lobbys[conn["lobby"]].remove(conn)
                    lobby_mate = self.lobbys.pop(conn["lobby"])[0]
                    lobby_mate["lobby"] = None
                    
                    log(f'updated and notified affected lobby (lobby nr. {conn["lobby"]})',"<L>")

                    self.assign_lobby(lobby_mate)
                else:
                    log(f'this shouldn\'t (can\'t) happen! lobby nr. {conn["lobby"]} of conn {conn["conn"]} isn\'t in self.lobbys',"<L>")
            else:
                if self.waiting_for_lobby == conn:
                    self.waiting_for_lobby = None
                
            if len(self.connections) == 0:
                self.shutting_off = True
                self.shut_down_time = 30
                threading.Thread(target=self.shut_off_timer).start()
                log(f"!! Starting shutt off timer !! t: -{self.shut_down_time}s","*")
                    
    def assign_lobby(self,conn):
        if self.waiting_for_lobby != None:
            lobby_nr = self.lobby_counter
            self.waiting_for_lobby["lobby"] = lobby_nr
            conn["lobby"] = lobby_nr
            self.lobbys[lobby_nr] = [self.waiting_for_lobby, conn]
            log(f"waiting conn ('{self.waiting_for_lobby['addr']}') & new conn ('{conn['addr']}') now in lobby nr. {lobby_nr} | lobby count: {len(self.lobbys)}","<L>")
            self.waiting_for_lobby = None
            info = {'type': 'join'}
            self.notify_lobby(info,conn,True)
            self.lobby_counter += 1
        else:
            self.waiting_for_lobby = conn
            log(f"new conn ('{conn['addr']}') waiting for lobby (2. conn required for creation) | lobby count: {len(self.lobbys)}","<L>")

    def notify_lobby(self,data,conn,send_sender=False):
        log(f"trying to send {data} to lobby nr.: {conn['lobby']}","<S>")    
        for c in self.lobbys[conn["lobby"]]:
            if send_sender or c != conn:
                try:
                    c["conn"].sendall((json.dumps(data) + "\n").encode())
                except:
                    log(f"failed to send data: {data} to {c['addr']} | lobby {c['lobby']}","<err>")

    def receiver(self,conn,bits=1096):
        buffer = ""
        while self.loop:
            try:
                buffer += conn["conn"].recv(bits).decode()
            except Exception as err:
                log(f"\n{err}\n")
                break
            if "\n" in buffer:
                (message, buffer) = buffer.split("\n", 1)
                yield message
        self.unregister(conn)

    def connection_loop(self,conn):
        recv = self.receiver(conn)
        for message in recv:
            data = json.loads(message)
            log(f"received {data} from {conn['addr']}","<R>")
            self.notify_lobby(data,conn)

    def main_loop(self):
        log("main loop active.", "<gs>")
        while self.loop:
            try:
                conn, addr = self.socket.accept()
                new_conn = {"conn" : conn, "addr" : addr, "lobby" : None}
                self.register(new_conn)        
                threading.Thread(target=self.connection_loop,args=([new_conn])).start()                
            except Exception as err:
                pass
                #log(f"\n{err}\n")
                #log(f"!! error whilst establishing a connection !! num_conns: {len(self.connections)} (open threads: {threading.active_count()})","<err>")
        log("main loop terminated.", "<gs>")

    def input_loop(self):
        while self.loop:
            inp = input("inp: ")
            if inp == "/c":
                self.close()

if __name__ == "__main__":
    server = GameServer()
    #threading.Thread(target=server.input_loop).start()
    server.main_loop()
