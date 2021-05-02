import curses
import threading
import time
from datetime import datetime
import os


def debug(msg):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    with open(os.getcwd() + '\\debuglog.txt', 'a', encoding='utf-8') as file:
        file.write(current_time + '  --- ' + str(msg) + '\n')
        file.close()


class Clock(threading.Thread):
    """ Clock curses string class. Updates every second. Easy to install """

    def __init__(self, stdscr, y, x, show_seconds=True):
        """ Create the clock """
        super(Clock, self).__init__()
        if show_seconds:
            self._target=self.update_seconds
        else:
            self._target=self.blink_colon
        self.y = y
        self.x = x
        self.daemon = True
        self.stdscr = stdscr
        self.start()

    def update_seconds(self):
        """ If seconds are showing, update the clock each second """
        while 1:
            self.stdscr.addstr(self.y, self.x, time.strftime("%a, %d %b %Y %H:%M:%S"))
            self.stdscr.refresh()
            time.sleep(1)

    def blink_colon(self):
        """ If seconds are not showing, blink the colon each second """
        while 1:
            if int(time.time()) % 2 != 0:
                self.stdscr.addstr(self.y, self.x, time.strftime("%a, %d %b %Y %H:%M"))
            else:
                self.stdscr.addstr(self.y, self.x, time.strftime("%a, %d %b %Y %H %M"))
            stdscr.refresh()
            time.sleep(1)

    def redraw(self, stdscr, x):
        self.stdscr = stdscr
        text = time.strftime("%a, %d %b %Y %H:%M:%S")
        self.stdscr.addstr(self.y, x, text)
        self.x = x
        self.stdscr.refresh()

class Textbox():
    def __init__(self, stdscr, y, x, text=None):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        if text == None:
            self.text = ''
        else:
            self.text = text
            self.rewrite(self.text)

    def key_input(self, key):
        if key == 8:
            self._delete()
        else:
            try:
                self.text = self.text + chr(key)
                self.rewrite(self.text.strip())
            except:
                pass

    def _delete(self):
        self.text = self.text[:-1]
        self.rewrite(' ' * (len(self.text)+1))
        self.rewrite(self.text)
    def empty(self):
        self.rewrite(' ' * (len(self.text)+1))
        self.text = ''




    def rewrite(self, text):
        #print('TEXT:' + text)
        self.stdscr.addstr(self.y, self.x, text)
        self.stdscr.refresh()




class PasswordTextbox(Textbox):
    def _delete(self):
        self.text = self.text[:-1]
        self.stdscr.addstr(self.y, self.x, ' ' * (len(self.text)+1))
        self.stdscr.refresh()
        self.rewrite(self.text)
    def rewrite(self, text):
        self.stdscr.addstr(self.y, self.x, '*' * len(self.text))
        self.stdscr.refresh()

class AdvancedTextbox(Textbox):
    def __init__(self, stdscr, y, x, highlight={}, highlight_words={}):
        super().__init__(stdscr, y, x)
        self.highlight = highlight
        self.highlight_words = highlight_words

        color_list = [curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_CYAN, curses.COLOR_RED, curses.COLOR_MAGENTA, curses.COLOR_YELLOW, curses.COLOR_WHITE]
        for i in range(7):
            curses.init_pair(i+1, color_list[i], curses.COLOR_BLACK)

    def rewrite(self, text):
        x_val = self.x

        for char in text:

        
            if char in self.highlight:
                highlight = self.highlight[char]
                self.stdscr.addstr(self.y, self.x, char, curses.color_pair(highlight))
                self.x += 1
            else:
                self.stdscr.addstr(self.y, self.x, char)
                self.x += 1
        self.x = x_val
        '''
        self._delete()
        found = True
        for char in text:
            if found == False:
                self.stdscr.addstr(self.y, self.x, char)
                self.x += 1
            found = False
            for word in self.highlight_words.keys():

                gen = 0
                if found == True:
                    break
                while True:
                    if char == word[gen]:
                        gen += 1
                        if gen == len(word):
                            found = True
                            color = int(self.highlight_words[word])
                            self.stdscr.addstr(self.y, self.x, word, curses.color_pair(color))
                            self.x += len(word)
                    else:
                        break
        '''



class Message():
    def __init__(self, stdscr, y, x, user, text):
        color_list = [curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_CYAN, curses.COLOR_RED, curses.COLOR_MAGENTA, curses.COLOR_YELLOW, curses.COLOR_WHITE]
        for i in range(7):
            curses.init_pair(i+1, color_list[i], curses.COLOR_BLACK)

        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.user = user
        self.text = text

        self.resize(self.y, self.x)

    def resize(self, y, x):
        self.y = y
        self.x = x

        self._delete()

        self.add_username()
        self.add_message()

        self.stdscr.refresh()
    def add_username(self):
        self.stdscr.addstr(self.y, self.x, self.user, curses.color_pair(5))
        self.stdscr.refresh()
    def add_message(self):
        self.stdscr.addstr(self.y, (self.x+len(self.user)+1), self.text, curses.color_pair(2))
        self.stdscr.refresh()
    def _delete(self):
        self.stdscr.addstr(self.y, self.x, ' ' * (len(self.user) + len(self.text)))

class Scrollpad():
    def __init__(self, scr, lines, columns, uy=0, ux=0, dy=25, dx=25):
        color_list = [curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_CYAN, curses.COLOR_RED, curses.COLOR_MAGENTA, curses.COLOR_YELLOW, curses.COLOR_WHITE]
        for i in range(7):
            curses.init_pair(i+1, color_list[i], curses.COLOR_BLACK)

        self.scr = scr

        self.lines = lines # Should be a big value
        self.columns = columns #If I would use also vertical scroll

        self.uy = uy
        self.ux = ux
        self.dy = dy
        self.dx = dx

        self.pad_pos_y = 0

        self.pad = curses.newpad(self.lines, self.columns);
        self.pad.scrollok(True)

        self.content = []

    def refresh(self):
        # from y character; from x character; upper y; upper x; bottom y; bottom x;
        self.pad.refresh(self.pad_pos_y, 0, self.uy, self.ux, self.dy, self.dx)
        self.scr.refresh()
        # TODO: Only use minus if you dont do it in your main program 
    def input(self, key):
        #print(self.pad.getyx()[0])
        if key == curses.KEY_DOWN and self.pad_pos_y < self.pad.getyx()[0] - 1:
            self.pad_pos_y += 1
            
            self.refresh()
        elif key == curses.KEY_UP and self.pad_pos_y > 0:
            self.pad_pos_y -= 1
            self.refresh()
        #elif key == curses.KEY_RESIZE:           
        #    while self.pad_pos_y > self.pad.getyx()[0] - self.lines - 1:
        #        self.pad_pos_y -= 1
        #    self.refresh()
        #    #pass

    def add_text(self, line, color=7, persistence=True):
        self.pad.addstr(line, curses.color_pair(color))
        if persistence == True:
            self.content.append(line)
            self.content.append(color)
        self.refresh()
        '''
        for i in range(0, 33):
            self.pad.addstr("{0} This is a sample string...\n".format(i))
            if i > height: 
                self.pad_pos = min(i - height, mypad_height - height)
            mypad_refresh()
        #time.sleep(0.05)
        '''


    def load_file(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                self.add_text(line)

        f.close()

    def resize(self, lines, columns, uy, ux, dy, dx):
        self.lines = lines # Should be a big value
        self.columns = columns #If I would use also vertical scroll

        self.uy = uy
        self.ux = ux
        self.dy = dy
        self.dx = dx

        self.pad = curses.newpad(self.lines, self.columns);
        self.pad.scrollok(True)
        self.pad_pos_y = 0

        self.reload_text()

    def reload_text(self):
        for i in range(len(self.content)):
            if i % 2 == 0 or i == 0:
                self.add_text(self.content[i], self.content[i+1], persistence=False)
                self.refresh()


class AdvancedScrollpad(Scrollpad):
    def __init__(self, scr, lines, columns, uy=0, ux=0, dy=25, dx=25):
        self.item_name = None
        super().__init__(scr, lines, columns, uy=0, ux=0, dy=25, dx=25)

    def input(self, key):
        #print(self.pad.getyx()[0])
        if key == curses.KEY_DOWN and self.pad_pos_y < len(self.content)/2:
            self.pad_pos_y += 1
            try:
                self.name = self.content[self.pad_pos_y*2]
            except IndexError:
                self.name = self.content[-2]
            print(self.name)
            self.refresh()
        elif key == curses.KEY_UP and self.pad_pos_y > 0:
            self.pad_pos_y -= 1
            self.name = self.content[self.pad_pos_y*2]
            print(self.name)
            self.refresh()




class Button():
    def __init__(self, y, x, height, width, title, stdscr):
        color_list = [curses.COLOR_WHITE, curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_CYAN, curses.COLOR_RED, curses.COLOR_MAGENTA, curses.COLOR_YELLOW, curses.COLOR_WHITE]
        pair = 1
        for background in range(8):
            for foreground in range(8):
                curses.init_pair(pair, color_list[foreground], color_list[background])
                pair += 1
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.title = title
        self.stdscr = stdscr
        self.draw()
    def on_click(self, key):
        _, x, y, _, _ = curses.getmouse()
        print('self.x: %s, x: %s, self.y: %s, y: %s' % (self.x, x, self.y, y))
        print(x >= self.x)
        print(x <= self.width)
        if x >= self.x and x <= (self.x + self.width):
            print('OK 1')
            if y >= self.y and y <= (self.y + self.height):
                self.highlight()

    def draw(self):
        y = self.y
        if self.height > 1:
            print(self.x)
            for i in range(self.height):
                if round(self.height/2) == i:
                    title_start_x = round(self.width/2)-round(len(self.title)/2)
                    if len(self.title) + title_start_x > self.width:
                        title = self.title[:(2*title_start_x)]
                    self.stdscr.addstr(y, self.x + title_start_x, self.title)
                else:
                    self.stdscr.addstr(y, self.x, '#'*self.width)
                y += 1
        else:
            title_start_x = round(self.width/2)-round(len(self.title)/2)
            if len(self.title) + title_start_x > self.width:
                title = self.title[:(2*title_start_x)]
            self.stdscr.addstr(y, title_start_x, self.title)




    def highlight(self):
        print('highlight')
        self._delete()

    def _delete(self):
        for y in range(self.height):

            self.stdscr.addstr(self.y + y, self.x, ' '*self.width)

