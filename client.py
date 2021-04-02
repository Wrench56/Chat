import socket
import threading
import time

class Client():
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.username = 'MYGOD123'

        self.success = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.connect()


    def connect(self):
        while self.success != True:
            try:
                self.socket.connect((self.host, self.port))

            except BlockingIOError:
                pass
            except OSError:
                self.success = True
                break
        self.socket.send(b'$username:' + self.username.encode() + b'$')
        time.sleep(1.0)
        try:
            reply = self.socket.recv(1024).decode()
            if reply == '$not_valid_username$':
                print('Error: Not Valid Username')
                exit()
            elif reply.startswith('$welcome$'):
                print('Username accepted, everything seems to be alright!')
                threading.Thread(target=self.recv).start()
                #threading.Timer(10.0, )
        except BlockingIOError:
            pass
    def send(self, msg):
        self.socket.send(msg.encode())
    def recv(self):
        while True:
            try:
                self.msg = self.socket.recv(1024).decode()
                print(self.msg)
            except BlockingIOError:
                pass

if __name__ == '__main__':
    c = Client()
