import socket
import threading
import time

class Server():
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port

        self.clients = []
        self.users = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        #self.socket.settimeout(2000)

        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        threading.Thread(target=self.accept_conntection).start()
        threading.Thread(target=self.receive_messages).start()
    def accept_conntection(self):
        while True:
            try:
                client_socket, client_address = self.socket.accept()
                self.clients.append(client_socket)
                print('New accepted connection from %s' % client_address[0])
            except BlockingIOError:
                pass


    def receive_messages(self):
        while True:
            for client in self.clients:
                try:
                    self.msg = client.recv(1024).decode()
                    if self.msg:
                        print(self.msg)
                        if self.msg.startswith('$') and self.msg.endswith('$'):
                            self.check_for_special_msg(self.msg, client)
                        else:
                            print(self.msg)
                            self.broadcast(self.msg)
                except BlockingIOError:
                    continue
    def check_for_special_msg(self, msg, client):
        msg = msg.replace('$', '')
        if msg.startswith('username:'):
            msg = msg.replace('username:', '')
            if msg in self.users:
                client.send(b'$not_valid_username$')
            else:
                print('Username accepted!')
                client.send(b'$welcome$')
                self.users[client] = msg
    def broadcast(self, msg):
        for socks in self.clients:
            socks.send(msg.encode())

s = Server()