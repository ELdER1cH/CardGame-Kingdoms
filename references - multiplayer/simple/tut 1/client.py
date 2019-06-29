# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
s.connect(('93.227.151.107', 6789)) 
  
# receive data from the server 
print(s.recv(1024))
# close the connection 
s.close()  
