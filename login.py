#login form

import curses
import gui
import curses_util
import client
import os


try:
	os.popen('title 5pyd3r login')
except:
	pass

def start():
	pass

def labels(stdscr):
	stdscr.addstr(3, 2, "Server's IP:")
	stdscr.addstr(6, 2, "Username:")
	stdscr.addstr(9, 2, "Passwords:")

def draw_curs(stdscr, status):
	if status == 0:
		stdscr.move(3, 15)
	elif status == 1:
		stdscr.move(6, 15)
	elif status == 2:
		stdscr.move(9, 15)

	stdscr.refresh()

def main(stdscr):
	status = 0
	stdscr.border(0)
	curses.noecho()

	y, x = stdscr.getmaxyx()
	
	labels(stdscr)
	server_tb = curses_util.AdvancedTextbox(stdscr, 3, 15, highlight={'.': 5, ':':5, '0':2, '1': 2, '2':2, '3':2, '4':2, '5':2, '6':2, '7':2, '8':2, '9': 2})
	username_tb = curses_util.Textbox(stdscr, 6, 15)
	password_tb = curses_util.PasswordTextbox(stdscr, 9, 15)
	stdscr.move(3, 15)
	while True:
		key = stdscr.getch()
		if key == curses.KEY_F1:
			exit()
		elif key == curses.KEY_RESIZE:
			stdscr.erase()
			stdscr.border(0)
			labels(stdscr)
			server_tb.rewrite(server_tb.text)
			username_tb.rewrite(username_tb.text)
			password_tb.rewrite(password_tb.text)
		elif key == curses.KEY_ENTER or key == 13 or key == 10:
			server = server_tb.text.split(':')
			if server[0] == '':
				payload = ['127.0.0.1']
			else:
				payload = [server[0]]
			try: 
				if server[1] == '':
					payload.append('55555')
				else:
					payload.append(server[1])
			except:
				payload.append('55555')
			if username_tb.text == '':
				payload.append('G')
			else:
				payload.append(username_tb.text)
			if password_tb.text == '':
				payload.append('password')
			else:
				payload.append(password_tb.text)
			print(payload)
			client_obj = client.Client(host=payload[0], port=payload[1], username=str(payload[2]), password=str(payload[3]))
			gui.start(client_obj)
		elif key == curses.KEY_DOWN:
			if status != 2:
				status += 1
				draw_curs(stdscr, status)
		elif key == curses.KEY_UP:
			if status != 0:
				status -= 1
				draw_curs(stdscr, status)
		else:
			if status == 0:
				server_tb.key_input(key)
			elif status == 1:
				username_tb.key_input(key)
			elif status == 2:
				password_tb.key_input(key)


#if __name__ == '__main__':
start()
curses.wrapper(main)