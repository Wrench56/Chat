#!/usr/bin/env python2

import curses
import time
import curses_util

mypad_contents = []

def main(scr):
  # Create curses screen
  scr.keypad(True)
  curses.noecho()
  scr.refresh()

  scroll = curses_util.AdvancedScrollpad(scr, 1000, 100)
  scroll.refresh()
  scroll.load_file('C:\\Exes\\valorant_helper.py')
  scroll.add_text("\nWelcome LOL", 2)
  running = True
  while running:
    ch = scr.getch()
    scroll.input(ch)
    if ch < 256 and chr(ch) == 'q':
      running = False
  # Store the current contents of pad

curses.wrapper(main)
# Write the old contents of pad to console
#print('\n'.join(mypad_contents))