from output import *


def main(stdscr):
    major = Output()
    major.main_func()


curses.wrapper(main)