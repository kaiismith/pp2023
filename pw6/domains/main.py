from output import *


def main(stdscr):
    output = Output()
    output.main_func()


curses.wrapper(main)