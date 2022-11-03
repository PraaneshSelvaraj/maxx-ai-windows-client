import sys
from PySide2 import QtWidgets, QtGui
import webbrowser
import pickle
import os
import socket

data = {}
encoding = 'ascii'
buffer = 1024
#getting name ip and port
if os.path.exists('data.pickle'):
    data = pickle.load('data.pickle')
else:
    for num,arg in enumerate(sys.argv):
        if arg == '-name':
            data['name'] = sys.argv[num+1]
            
        elif arg == '-ip':
            data['ip'] = sys.argv[num+1]

        elif arg == '-port':
            data['port'] = int(sys.argv[num+1])

#Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(10)
client.connect((data['ip'], data['port']))

message = client.recv(buffer).decode(encoding)

if message == 'NICKNAME':
    #sending nickname
    msg=data['name']+"~"+'None'
    client.send(msg.encode(encoding))

client.settimeout(None)
message = client.recv(buffer).decode(encoding)
client.settimeout(10)

print(message)
if message == 'CONNECTIONACCEPTED':
    print("Connected to server")
    hsh = client.recv(buffer).decode(encoding)
    print("HASH : {}".format(hsh))
    print("Listening for commands")

elif message == '!Name':
    print("NAME ALREADY CHOSEN")

else:
    print('Connection Refused')
    exit()

while True:
    try:
        message = client.recv(buffer).decode(encoding)
        print(message)

        if message == '!DISCONNECT':
            #Server asks to disconnect
            client.send("DISCONNECTED".encode(encoding))
            client.close()
            print("Client Disconnecte")
            exit()
        
        elif message == '!ALIVE':
            #Server checking if client is connected.
            client.send("ALIVE".encode(encoding))

        else:
            #Commands send by server
            return_msg = "FALSE"
            task, msg = message.split("~")
            
            if task == 'WEBBROWSER':
                #opening the link using webbrowser
                webbrowser.open(msg)
                return_msg ='TRUE'
               
            client.send(return_msg.encode(encoding))

    except Exception as e:
        if "timed out" in "{}".format(e):
            continue
        else: print("EXCEPTION: {}".format(e))
