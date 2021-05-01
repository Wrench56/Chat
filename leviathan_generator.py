#username_generator

import colorama
import os
from termcolor import colored, cprint
import pyfiglet
import platform
from datetime import datetime
import requests
import socket
import time


VERSION = 1.0

colorama.init()

print()
print()

def connection():
	try:
		requests.get('https://google.com', timeout=1.0)
		return True
	except requests.exceptions.ConnectTimeout:
		return False
	except requests.exceptions.ConnectionError:
		return False

with open(os.getcwd() + '\\spider.txt', 'r', encoding='utf-8') as leviathan_file:
	while True:
		try:
			if leviathan_file.readline() == '':
				break
			else:	
				cprint(leviathan_file.readline().strip('\n')) #None
		except EOFError:
			break

header = pyfiglet.figlet_format('   5pyd3r')
cprint(header, 'red')

cprint('                  Join the DarkWeb!', 'red')
print('='*40)
time.sleep(2.0)
print()
print('+' + 16*'-' + ' INFO ' + 16*'-' + '+')
now = datetime.now()
# dd/mm/YY H:M:S
payload = now.strftime(" Time: %d-%m-%Y %H:%M:%S")
spaces = 38 - len(payload)
print('|' + str(payload) + spaces*' ' + '|')
payload = ' User: '
payload = payload + os.popen('whoami').read().replace('\n', '')

spaces = 38 - len(payload)
print('|' + str(payload) + spaces*' ' + '|')
payload = ' Current version: '
payload = payload + str(VERSION)

spaces = 38 - len(payload)
print('|' + str(payload) + spaces*' ' + '|')
payload = ' Connection: '
conn = connection()
payload = payload + str(conn)
spaces = 38 - len(payload)
print('|' + str(payload) + spaces*' ' + '|')
payload = ' IP: '
payload = payload + socket.gethostbyname(str(socket.gethostname()))
spaces = 38 - len(payload)
print('|' + str(payload) + spaces*' ' + '|')
payload = ' Platform: '
payload = payload + platform.system()
spaces = 38 - len(payload)
print('|' + str(payload) + spaces*' ' + '|')
payload = ' Release: '
payload = payload + platform.release()
spaces = 38 - len(payload)
print('|' + str(payload) + spaces*' ' + '|')
print('+' + 38*'-' + '+')
print()
time.sleep(0.1)
print('[+] Checking for new 5pyd3r release...')




