import socket
import sys, json
import datetime
import threading
import time

"""import os
import psutil
process = psutil.Process(os.getpid())
print(process.memory_percent())
print(process.cpu_percent())
print(process.num_threads())
print(process.threads())
print(process.status())

while True:
    pass"""

"""lis = {0:1,2:3,4:5}
lis3 = [1,2,3]
print(len(lis))
print(len(lis3))
lis2 = lis.copy()
print(lis)
val = lis.pop(0)
print(lis)
print(val)
print(lis2)"""

"""info = {'type': 'lobbyprecaution','lobby': 0}
i2 = json.dumps(info)
i3 = i2.encode()
i4 = i2 + "\n"
i5 = i4.encode()

z = i5.decode()
z1 = json.loads(z)["type"]
z2 = z.split("\n")
z3 = json.loads(z2[0])["type"]

print(info)
print(i2)
print(i3)
print(i4)
print(i5)

print(z)
print(z1)
print(z2)
print(z3)"""

HEADERSIZE = 10
run = True

#msg = str(datetime.datetime.now()) +"test"
#print(msg)
msg = {'type': 'lobbyprecaution','lobby': 1}
host = "127.0.0.1"      
port = 6789             

s = socket.socket()
s.connect((host, port))

def send():
    s.sendall(json.dumps(msg).encode())

#inp = input(">num connections: ")

def recv_loop():
    global run
    while run:       
        try:
            r = s.recv(1096).decode()
            print(r)
        except Exception as err:
            print(err)
            print("Error whilst fetching server messages!")
            run = False
            break
            

#recv_loop()



