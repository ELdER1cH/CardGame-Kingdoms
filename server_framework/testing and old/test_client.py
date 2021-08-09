import socket
import sys, json, datetime, time
import threading
import random

run = True
sockets = []
nr = 0
msg = "hello world\n"#str(datetime.datetime.now()) +"test" #print(msg) #msg = {'type': 'lobbyprecaution','lobby': 1}
host = "127.0.0.1"      
port = 29428 #6789                   

def connection(socket,nr):
    global run
    while run:
        try:
            msg = socket.recv(1096).decode()
            print(str(nr) + ": got msg " + str(msg) + "\n")
        except Exception as err:
            #print(err)
            print("Error whilst fetching server messages!")
            socket.close()
            break

def new_socket():
    global nr
    s = socket.socket()
    s.connect((host, port))
    nr += 1
    sockets.append(s)
    thr = threading.Thread(target=connection,args=([s,nr]))#, daemon=True 
    thr.start()

if __name__ == "__main__":
    while run:
        inp = input("/n - new connection | /t - terminate one connection | /s - random socket sends msg | /c - close\n")
        if inp == "/n":
            new_socket()            
        elif inp == "/t":
            so = sockets.pop(0)
            so.close()

        elif inp == "/s":
            l = len(sockets)
            ri = random.randint(0,l-1)
            sockets[ri].sendall(msg.encode())
            print(f"{ri} send {msg}\n")
            
        elif inp == "/c":
            run = False
            for soc in sockets:
                soc.close()
            while threading.active_count() > 2: # this simply does it, that red >>> appears in console after
                pass                            # errors/ messages from terminating threads (/ main threads terminates last ^^)

        elif inp == "/m": #many -> 50 conns
            for i in range(50):
                new_socket()


#new_server.py -> /t -> sometimes it misses, that a socket is closed... wonder if this could happen
                #with a real client.. why is this happening?? ..
                #-> /c -> it only registers that 8/50 are gone, altough all are gone!

#25 connections -> /c -> all stopped without erros (serversside too! ^^)


#https://realpython.com/intro-to-python-threading/#using-a-threadpoolexecutor

#https://www.programiz.com/python-programming/methods/built-in/enumerate
#https://stackoverflow.com/questions/6319207/are-lists-thread-safe

#https://realpython.com/python-concurrency/
#https://realpython.com/async-io-python/
