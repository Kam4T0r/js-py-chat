import urllib.request #to make get request
import websockets.sync.client as ws #to connect to websocket
import threading #multithreading
#to avoid text getting over
from prompt_toolkit import prompt 
from prompt_toolkit.shortcuts import print_formatted_text

res = urllib.request.urlopen('https://utilsy.glitch.me/rat.txt').read() #make get request
IP =  str(res).replace('b','').replace(r"'",'') #get ony IP of server

try:
    with ws.connect(f'ws://{IP}:2208') as socket: #connect to server IP on port 2208 using websocket protocol
        print('Connection established') #log
        usrName = str(input('Enter your username\n>')); #ask for username
        #avoid SERVER username so nobody trolls
        if usrName == 'SERVER':
            print("there cannot be any user named SERVER")
            exit(0)
        socket.send(f'[SERVER] User "{usrName}" joined the chat') #send msg to server.js that usrName joined
        def wait(): #define function that waits for messages from server
            while True:
                print_formatted_text(f"{socket.recv()}\n",flush=True,end='') #print message fetched from server.js
                print('',end='',flush=True) #flush stdout
        waitT = threading.Thread(target=wait) #make new thread
        waitT.start() #start new thread
        while True: #take input 4ever from user and send it to server so it can be displayed
            msg = prompt('>') #take input
            if msg.strip() == 'exit':
                exit(0)
            socket.send(f'[{usrName}] {msg}') #send message to server.js
except:
    print("Couldn't establish connection") #log error
"""
there are 2 threads, 1 with function wait so it can display messages the moment server sends it here

main thread takes input and sends it to server

waitT only waits for messages from server and displays it so sending and receiving works in parallel
"""