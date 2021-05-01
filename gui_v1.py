import curses
import time

class Window():
	def __init__(self, stdscr):
		self.stdscr = stdscr
		curses.noecho()
		curses.cbreak()
		self.stdscr.keypad(True)

		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)

		self.main()
	def main(self):
		#height,width = self.stdscr.getmaxyx()
		#print(height, width)
		self.stdscr.addstr(2, 2, "Hello")
		self.stdscr.addch(4,10,curses.ACS_LRCORNER)
		self.stdscr.refresh()
		time.sleep(2.0)
		self.delete()
	def delete(self):
		exit()

def main(stdscr):
	obj = Window(stdscr)
if __name__ == '__main__':
	curses.wrapper(main)