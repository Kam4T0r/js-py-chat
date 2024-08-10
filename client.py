import urllib.request
import websockets.sync.client as ws
import threading

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
                print(f"{socket.recv()}")
                print('>',end='',flush=True)
        waitT = threading.Thread(target=wait)
        waitT.start()
        while True:
            msg = str(input());
            socket.send(f'[{usrName}] {msg}')
except:
    print("Couldn't establish connection")