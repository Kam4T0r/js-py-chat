import urllib.request
import websockets.sync.client as ws
import threading
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import print_formatted_text

res = urllib.request.urlopen('https://utilsy.glitch.me/rat.txt').read()
IP =  str(res).replace('b','').replace(r"'",'')

try:
    with ws.connect(f'ws://{IP}:2208') as socket:
        print('Connection established')
        usrName = str(input('Enter your username\n>'));
        if usrName == 'SERVER':
            print('there cannot be any user named server')
            exit()
        socket.send(f'[SERVER] User "{usrName}" joined the chat')
        def wait():
            while True:
                print_formatted_text(f"{socket.recv()}\n",flush=True,end='')
                print('',end='',flush=True)
        waitT = threading.Thread(target=wait)
        waitT.start()
        while True:
            msg = prompt('>')
            socket.send(f'[{usrName}] {msg}')
except:
    print("Couldn't establish connection")