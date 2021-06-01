import curses
from curses import textpad
import os
import threading
import traceback
import time

import client
import curses_util


class GUI():
	def __init__(self, stdscr):
		global client_obj
		self.client_obj = client_obj
		self.username = 'G'
		self.password = 'password'

		self.y = 10
		self.msg_list = []	

		threading.Thread(target=self.receive_msg).start()

		self.to = '$user$:G:'
		self.msg = ''
		self.last_msg = 'Nothing'

		curses.noecho()
		curses.curs_set(0)
		#curses.mousemask(1) #do not show cursor on click (turn off for debugging)
		curses.start_color()

		self.stdscr = stdscr
		self.stdscr.erase()
		#self.stdscr.nodelay(1)

		y, x = self.stdscr.getmaxyx()

		x1 = round((x/12)*3)
		x2 = x1 + round((x/12)*7)

		self.tab_focus = 'dashboard'


		self.draw_widgets(init = True)

		self.main()

	def draw_widgets(self, init=False):

		self.stdscr.erase()

		y, x = self.stdscr.getmaxyx()
		print(y, x)

		x1 = round((x/12)*3)
		x2 = x1 + round((x/12)*7)
		height_chats = round(y/2)
		groups_height = y - height_chats


		self.status_bar = self.stdscr.subwin(2, round((x/12)*7), 0, x1)
		self.status_bar.box()
		self.text_box_bar = self.stdscr.subwin(3, round((x/12)*7), round(y)-3, x1) #rows, columns, y, x 
		self.text_box_bar.box()
		self.main_win = self.stdscr.subwin(round(y)-5, round((x/12)*7), 2, x1)
		self.main_win.box()
		try:
			self.active_users_win = self.stdscr.subwin(round(y), round((x/12)*2), 0, x2)
		except curses.error:
			self.active_users_win = self.stdscr.subwin(round(y), round((x/12)*2), 0, x2-1)
		self.active_users_win.box()

		'''
		Chats and Groups
		'''
		self.chats_win_chats = self.stdscr.subwin(height_chats, round((x/12)*3), 0, 0) #rows, columns, y, x 
		self.chats_win_chats.box()

		self.chats_win_groups = self.stdscr.subwin(groups_height, round((x/12)*3), height_chats, 0) #rows, columns, y, x 
		self.chats_win_groups.box()
		self.stdscr.addstr(0, 2, 'Chats')
		self.stdscr.addstr(height_chats, 2, 'Groups')


		if init == True:
			self.clock = curses_util.Clock(self.stdscr, 0, round((x/12)*3 + 2))
			self.tb = curses_util.Textbox(self.stdscr, round(y)-2, x1+1)
			self.dashboard = curses_util.Scrollpad(self.stdscr, 1024*1024, round((x/12)*7)-2, uy=3, ux=(x1+1), dy=round(y)-6, dx=(x1+1)+round((x/12)*7)-3)
			self.chats_dashboard = curses_util.AdvancedScrollpad(self.stdscr, 1024*1024, round((x/12)*3)-3, uy=2, ux=2, dy=height_chats-2, dx=round((x/12)*3)-3)
			#self.chats_dashboard.load_file(os.getcwd() + '\\chats.txt')
		self.dashboard.resize(lines=(1024*1024), columns=(round((x/12)*7)-2), uy=3, ux=(x1+1), dy=round(y)-6, dx=(x1+1)+round((x/12)*7)-3)
		self.chats_dashboard.resize(lines=(1024*1024), columns=(round((x/12)*3)-3), uy=2, ux=2, dy=height_chats-2, dx=round((x/12)*3)-3)
		textbox_text = self.tb.text
		#print(textbox_text)
		self.tb = None
		self.tb = curses_util.Textbox(self.stdscr, round(y)-2, x1+1, text=textbox_text)
		self.tb.rewrite(textbox_text)


		'''
		Status bar
		'''
		self.clock.redraw(self.stdscr, round((x/12)*3 + 2))

		self.stdscr.refresh()
	def receive_msg(self):

		while True:
			time.sleep(0.0001)
			self.msg = self.client_obj.msg
			#print(self.msg)


			if self.msg != None and self.last_msg != self.msg:
				print(self.msg)
				self.last_msg = self.msg
				print('Processing...')

				user_list = self.msg.split('@', 1)
				user = user_list[0]
				msg_list = user_list[1].split(':', 1)
				where = msg_list[0]
				msg = msg_list[1]
				y, x = self.stdscr.getmaxyx()
				self.y += 2
				self.x = round((x/12)*3)
				print(user, msg)
				'''
				Format msg
				'''

				self.msg = self.msg.replace('\\n', '\n')


				self.dashboard.add_text(str(user) + ': ', 4)
				self.dashboard.add_text(str(msg), 2)
				self.stdscr.refresh()
				


	def main(self):
		try:
			self.draw_widgets()
			while True:
				time.sleep(0.0001)
				key = self.stdscr.getch()
				print(key)
				if self.tab_focus == 'dashboard':
					self.dashboard.input(key)
				elif self.tab_focus == 'chats':
					self.chats_dashboard.input(key)
				elif self.tab_focus == 'groups':
					pass
				else:
					self.tab_focus = 'dashboard'

				#print('INPUT')
				
				if key != curses.KEY_RESIZE:# and key != curses.KEY_UP and key != curses.KEY_DOWN:
					if key == 351:
						if self.tab_focus == 'dashboard':
							self.tab_focus = 'chats'
						elif self.tab_focus == 'chats':
							self.tab_focus = 'groups'
						elif self.tab_focus == 'groups':
							self.tab_focus = 'dashboard'
						else:
							self.tab_focus = 'dashboard'
					if key == curses.KEY_MOUSE:
						pass
					if key != curses.KEY_UP and key != curses.KEY_DOWN and key != curses.KEY_MOUSE and key != 351:
						self.tb.key_input(key)
					#self.stdscr.refresh()
					#self.stdscr.doupdate()
					#print(key) #for debugging
					if key == 289:# or curses.KEY_F1: #for debugging
						break

					elif key == 8:
						#self.draw_widgets()
						pass
					elif key == curses.KEY_ENTER or key == 10 or key == 13:
						self.client_obj.to = self.to
						self.client_obj.send(self.tb.text)
						self.dashboard.add_text('$YOU$' + ': ', 6)
						self.dashboard.add_text(str(self.tb.text), 3)
						self.tb.empty()
						

					else:
						pass
				else:
					curses.resize_term(0, 0)
					self.stdscr.erase()
					self.draw_widgets()

					#self.tb.key_input(key)
						#self.msg = self.msg + chr(key)
						#self.stdscr.addstr(30, len(self.msg), chr(key))
		except Exception as e:
			traceback.print_exc()
		curses.endwin()
		os._exit(1)

class Window():
	def __init__(self, stdscr, height, width, y, x):
		self.stdscr = stdscr
		self.win = self.stdscr.subwin(height, width, y, x)
	def redraw(self, height, width, y, x):
		self.win.erase()
		self.win = None
		self.win = self.stdscr.subwin(height, width, y, x)


def main():
	curses.wrapper(GUI)

def start(client_obj_):
	global client_obj
	client_obj = client_obj_
	main()
