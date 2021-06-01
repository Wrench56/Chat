#username_generator

import git
import colorama
import os
from termcolor import colored, cprint
import pyfiglet
import platform
from datetime import datetime
import requests
import socket
import time 
import shutil
from subprocess import call

VERSION = 0.9


DIR_DOWNLOAD = 'C:\\Users\\dmark\\Onedrive\\Documents\\'
DIR_REMOVE = DIR_DOWNLOAD + 'Chat\\'


colorama.init()

print()
print()

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def get_version():
	r = requests.get('https://raw.githubusercontent.com/Wrench56/Chat/main/VERSION.txt')
	return r.text

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
newest = float(get_version())

if VERSION < newest:
	print('[+] A new release is available!\n    Your version is %s and the newest version is %s' % (VERSION, newest))
	print('[?] Do you want to update to version %s? Consider \n    that using an older softver might cause bugs \n    or major issues. It can be crucial to update your softver.\n    If you experience any bugs, please update your softver. ' % (newest))
	while True:
		inp = input('[y]es or [n]o: ')
		if inp.lower() == 'y':
			print('[+] Deleting previous version (%s)...' % VERSION)
			
			shutil.rmtree(DIR_REMOVE, onerror=onerror)
			print('[+] Successfully deleted version %s!' % VERSION)
			print('[+] Downloading newest release...')
			git.Git(DIR_DOWNLOAD).clone('https://github.com/Wrench56/Chat')
			print('[+] Version %s downloaded!' % newest)
			print()

			break
		elif inp.lower() == 'n':
			print('[+] Continueing without the new update...')
			print('[!] If you have any problems, try to update your softver!')
			print()
			break
		elif inp.lower() == 'exit':
			exit()
		else:
			print('[!] That\' not a valid command! Please enter y for [y]es or n for [n]o')
else:
	print('[+] Everything is up to date!')
print('[+] Starting 5pyd3r...')

os.popen('py ' + DIR_REMOVE + ' login.py')