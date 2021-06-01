import socket
import threading
import time
import json
import hashlib
import base64
import cypher
from datetime import datetime
import os
import rsa
import pickle

def debug(msg):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    with open(os.getcwd() + '\\debuglog.txt', 'a', encoding='utf-8') as file:
        file.write(current_time + '  --- ' + msg + '\n')
        file.close()



class Client():
    UNLOCK = 'unlockCrypt'
    def __init__(self, host='127.0.0.1', port=55555, username='unkn0wn', password='password'):
        self.key = cypher.generate(self.UNLOCK)
        print(self.key)



        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.to = None

        self.success = False
        self.reply = None
        self.msg = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.setblocking(False)
        self.connect()


    def connect(self):
        while self.success != True:
            try:
                '''
                TODO : WARNING: I kinda had to use blocking here, because connections from outside are might not
                be so fast as from inside. (I had to learn it in the hard way:
                after 3hours of debugging i finally found it 23:13pm)
                '''
                self.exit_case = threading.Timer(10.0, self.timeout, args=('Connection not established',))
                self.exit_case.start()
                self.socket.setblocking(True)
                self.socket.connect((self.host, int(self.port)))
                self.exit_case.cancel()
                self.socket.setblocking(False)
                break
            except BlockingIOError:
                pass
        print(str(hashlib.sha256(self.password.encode()).hexdigest()))

        while True:
            try:
                msg = self.socket.recv(1024)
                if msg.startswith(b'$server$@$YOU$:$key$:'): # Can't decode private key obj, so just use byte structures
                    key = msg.replace(b'$server$@$YOU$:$key$:', b'')
                    #print(msg)
                    self.public_key = rsa.key.PublicKey.load_pkcs1(key, format='DER')
                    print(self.public_key)
                    break
            except BlockingIOError:
                pass

        while True:
            time.sleep(0.001)
            try:
                message = self.username.encode() + b'|pw:' + (hashlib.sha256(self.password.encode()).hexdigest()).encode() + b'|key:' + self.UNLOCK.encode()
                print(rsa.encrypt(message, self.public_key))
                self.socket.send(b'$unkn0wn$@$server$:$username:' + rsa.encrypt(message, self.public_key)) #TODO only place where protocol not used
                debug('OK')
                time.sleep(1.0)
           
                reply = self.socket.recv(1024)
                reply = str(cypher.decrypt(reply, self.key).decode())
                if reply == '$server$@$YOU$:$not_valid_username$':
                    print('Error: Not Valid Username or password. Maybe you are already signed in? ')
                    exit()
                elif reply.startswith('$server$@$YOU$:$welcome$'):
                    print('Username accepted, everything seems to be alright!')
                    self.verify()
                    threading.Thread(target=self.recv).start()
                    break
                else:
                    print('Access not granted!')
                    exit()
            except BlockingIOError:
                pass

    def verify(self):
        threading.Thread(target=self.send_and_reply, args=(self.username + '@$server$:$verify$',)).start()
        self.exit_case = threading.Timer(10.0, self.timeout, args=('Verifiy timed out',))
        self.exit_case.start()
        while True:
            time.sleep(0.0001)
            if self.reply != None:
                if self.reply.startswith('$server$@$YOU$:$verified$'):
                    self.exit_case.cancel()
                    self.reply = None
                    print('Server verified!')
                    break
    def send_and_reply(self, msg):
        self.encrypted_send(self.socket, msg.encode())
        while True:
            print('[!]SEND_AND_REPLY RUNNING')
            time.sleep(0.0001)
            try:
                response = self.socket.recv(1024)
                self.reply = cypher.decrypt(response, self.key).decode()
                if self.reply != '': #TODO : If not used, it will swallow some of the messages!!!
                    break            #TODO : Do not comment this out!!!
            except BlockingIOError:
                pass
    def send(self, msg):
        self.encrypted_send(self.socket, self.username.encode() + b'@' + self.to.encode() + msg.encode())
        #self.socket.send(self.username.encode() + b'@' + b'$user$:G:' + msg.encode())
    def encrypted_send(self, client, message):

        '''
        use xor encryption
        '''

        #print(cypher.encrypt(message, self.key))
        client.send(cypher.encrypt(message, self.key))



    def recv(self):
        while True:
            time.sleep(0.0001)
            try:
                response = self.socket.recv(1024)
                self.msg = cypher.decrypt(response, self.key).decode()
                #print(self.msg)
                if len(self.msg) == 0:
                    print('A problem occured. The server suddenly stopped responding to our messages! Goodbye :)')
                    exit()
                if self.msg:
                    self.debug_(self.msg)

                    
            except BlockingIOError:
                pass
                #print('BlockingIOError')
    def timeout(self, reason):
        print('Quitted for reason: %s' % reason)
        exit()
        
    def debug_(self, msg):
        print('MSG from client:' + msg)

if __name__ == '__main__':
    c = Client()
