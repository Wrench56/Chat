#test
import curses
import curses_util


def main(scr):
	curses.curs_set(0)
	curses.mousemask(1)

	b = curses_util.Button(1, 10, 1, 10, 'Hello', scr)
	running = True
	while running:
		ch = scr.getch()
		b.on_click(ch)
		if ch < 256 and chr(ch) == 'q':
			running = False





if __name__ == '__main__':
	curses.wrapper(main)