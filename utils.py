import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket
import threading

def get_key(val, dict):
    for key, value in dict.items():
         if val == value:
             return key
 
    return None





def compare(a, b):
    for x, y in zip(a, b):
        if x == y:
            print(x)

#compare('asd', 'asd')

def server_online(ip, port):
	a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	location = (ip, int(port))
	result_of_check = a_socket.connect_ex(location)

	if result_of_check == 0:
   		return True
	else:
   		return False

