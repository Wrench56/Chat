import socket
import threading
import time
import cypher
import utils
import os
import rsa
import pickle


class Server():
    UNLOCK = 'unlockCrypt'
    def __init__(self, host='', port=55555):


        self.key = self.UNLOCK

        self.host = host
        self.port = port

        self.msg_args = []
        self.clients = []
        self.users = {}
        self.all_users = {'H':'5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                          'G':'5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        #self.socSket.settimeout(2000)

        self.socket.bind((self.host, self.port))
        print('Running on %s on %s' % (self.host, self.port))
        self.socket.listen(1)
        threading.Thread(target=self.accept_conntection).start()
        threading.Thread(target=self.receive_messages).start()
        
    def accept_conntection(self):
        while True:
            time.sleep(0.0001)
            try:
                client_socket, client_address = self.socket.accept()
                public_key, private_key = rsa.newkeys(1024)

                #print(public_key)

                obj = User(client_socket, private_key)

                encoded_pubkey = public_key.save_pkcs1(format='DER')
                
                #print(encoded_pubkey.decode('ascii'))
                client_socket.send(b'$server$@$YOU$:$key$:' + encoded_pubkey)#bytes('$server$@$YOU$:$key$:', 'utf-8') + encoded_pubkey)
                self.clients.append(obj)
                #publicKey, privateKey = rsa.newkeys(512)
                #client_socket.send(b'key:' + publicKey)
                print('New accepted connection from %s' % client_address[0])
            except BlockingIOError:
                pass


    def receive_messages(self):
        while True:
            time.sleep(0.0001)

            for user in self.clients:
                socket = user.socket
                try:
                    #print(user.private_key)

                    self.msg = socket.recv(1024)
                    print(self.msg)
                    if self.msg.startswith(b'$unkn0wn$@$server$:$username:'):
                        if user.private_key != None:
                            print('DECRYPTION TIME!')
                            self.msg = self.msg.replace(b'$unkn0wn$@$server$:$username:', b'')
                            self.msg = '$unkn0wn$@$server$:$username:' + rsa.decrypt(self.msg, user.private_key).decode()
                    else:
                        self.msg = cypher.decrypt(self.msg, user.key).decode()


                    if len(self.msg) == 0:
                        print('User %s disconnected! Bye-bye!' % user.username)
                        self.clients.pop(self.clients.index(user))
                        try:
                            del self.users[user.username]
                        except KeyError:
                            pass
                            
                    if self.msg:
                        self.msg_args = self.msg.split('@', 1)
                        if self.msg_args[1].startswith('$server$:'):
                            self.check_for_special_msg(self.msg_args, socket, user)
                        else:
                            print(self.msg)
                            self.broadcast(self.msg)
                except BlockingIOError:
                    continue
                except ConnectionResetError:
                    print('User %s disconnected! Bye-bye!' % user.username)
                    self.clients.pop(self.clients.index(user))
                    try:
                        del self.users[user.username]
                    except KeyError:
                        pass

    def check_for_special_msg(self, msg_args, socket, user):
        msg = msg_args[1].replace('$server$:', '')
        if msg.startswith('$username:'):
            msg = msg.replace('$username:', '')
            msg_parts = msg.split('|')
            
            if msg_parts[0] == self.users:
                user.socket.send(socket, b'$server$@$YOU$:$not_valid_username$')
            elif msg_parts[0] in self.all_users:
                print('!!!!')
                print(self.all_users[msg_parts[0]])
                print(str(msg_parts[1]))
                msg_parts[1] = msg_parts[1].replace('pw:', '')
                if msg_parts[1] == self.all_users[msg_parts[0]] and msg_parts[2].startswith('key:'):
                    msg_parts[2] = msg_parts[2].replace('key:', '')
                    print('Username accepted!')
                    print(socket)
                    
                    user.username = msg_parts[0]
                    user.password = msg_parts[1]
                    user.key = cypher.generate(msg_parts[2])
                    print(user.key)

                    self.users[msg_parts[0]] = user
                    self.send_(user, b'$server$@$YOU$:$welcome$')

            else:
                self.send_(user, b'$server$@$YOU$:$not_valid_username$')
        elif msg_args[1].replace('$server$:', '').startswith('$verify$'):
            self.send_(user, b'$server$@$YOU$:$verified$')
    def broadcast(self, msg):
        print('Broadcasting...')
        sender_receiver = msg.split('@', 1)
        if sender_receiver[1].startswith('$user$:'):
            print('Found receiver!')
            user_msg = sender_receiver[1].replace('$user$:', '').split(':', 1)
            user = user_msg[0]
            msg = user_msg[1]
            if user in self.users:
                print('Forwarding message...')
                sender = sender_receiver[0]
                print(self.users[user])
                self.send_(self.users[user], (sender.encode() + b'@' + user.encode() + b':' + msg.encode()))
                print('Message sent...')



        elif sender_receiver[1].startswith('$group$:'):
            pass
        #for socks in self.clients:
        #    socks.send(msg.encode())
    def send_(self, user, message):
        '''
        Used to crypt the data and to make a safer use
        '''
        socket = user.socket
        key = user.key

        socket.send(cypher.encrypt(message, key))



class User():
    def __init__(self, socket, private_key=None):
        self.socket = socket
        self.private_key = private_key
        self.username = 'unkn0wn'

    def credentials(self, username, password):
        self.username = username
        self.password = password

    def set_key(self, key):
        self.key = key



if __name__ == '__main__':
    s = Server()