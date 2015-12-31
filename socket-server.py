import socket
import sys
from thread import *
from tasks import post
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(1)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #Receiving from client, receive data, pass it to redis queue and terminates the connection
    data = conn.recv(1024)
    if not data: 
        conn.close()

    #REST Url to call to add song to mongo database
    url = 'http://127.0.0.1:8000/addSong/'
    data = {'url' : data}
    result = post.delay(url, data)

    try:
        reply = 'Song url added to database'
        conn.sendall(reply)

    except socket.error, e:
        conn.close()
     
    #Close the connection
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()