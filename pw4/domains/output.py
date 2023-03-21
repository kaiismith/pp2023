import curses

from input import *


class Output:
    def __init__(self):
        # Object variables that keep track of what line they're in
        self.row1 = 12
        self.row2 = 12
        self.row3 = 12

        # Object variables that check whether students, courses, mark are already in the table or not
        self.last_student_id = []
        self.last_course_id = []
        self.last_mark = []

        # Create options for functions
        self.menu = ['Add Students', 'Add Courses', 'Add Marks', 'Display Marks', 'Calculate GPA', 'Sort GPA', 'Exit']

        # Object variables to get functions, classes from input.py
        self.getInput = Input()
        self.screen = curses.initscr()

    # Initialize the table
    def draw_table(self, start=12, end=20):
        text = [
            "[!] Made by BI12-406",
            "                                               .-')    .-') _    ('-. .-.                                               ",
            "                                              ( OO ). (  OO) )  ( OO )  /                                               ",
            "──────────────────────────────── ,--. ,--.   (_)---\_)/     '._ ,--. ,--. .---. .-----. ────────────────────────────────",
            "                                 |  | |  |   /    _ | |'--...__)|  | |  |/_   |/ ,-.   \                                ",
            "                                 |  | | .-') \  :` `. '--.  .--'|   .|  | |   |'-'  |  |                                ",
            "                                 |  |_|( OO ) '..`''.)   |  |   |       | |   |   .'  /                                 ",
            "                                 |  | | `-' /.-._)   \   |  |   |  .-.  | |   | .'  /__                                 ",
            "                                ('  '-'(_.-' \       /   |  |   |  | |  | |   ||       |                                ",
            "                                  `-----'     `-----'    `--'   `--' `--' `---'`-------'                                ",
            "            Courses            ┌─────────────────────── Students ───────────────────────┐             Marks             ",
            "───────────────────────────────│   ID   │                 Name               │   DOBs   │───────────────────────────────"
        ]

        for idx, row in enumerate(text):
            self.screen.addstr(idx, 0, row)

        for i in range(start, end + 1):
            self.screen.addstr(i, 0, "                               │        │                                    │          │                               ")
        self.screen.addstr(end, 0, "                               └────────────────────────────────────────────────────────┘                               ")

        self.screen.addstr(22, 0, "────────── Functions ───────────────────────────────────────────────────────────────────────────────────────────────────")
        for i in range(23, 29):
            self.screen.addstr(i, 0, "                               │                                                                                        ")

    # Print the options for functions
    def print_opts(self, selected_row_idx):
        for idx, row in enumerate(self.menu):
            x = 0
            y = 23 + idx
            if idx == selected_row_idx:
                self.screen.attron(curses.color_pair(1))
                self.screen.addstr(y, x, f"> {row}")
                self.screen.attroff(curses.color_pair(1))
            else:
                self.screen.addstr(y, x, f"> {row}")

        self.screen.refresh()

    # Display student information on the screen
    def display_student_info(self):
        self.getInput.get_student_info()

        # "pos" contains 3 positions (staring columns) to print after input ID, name, dob
        pos = [32, 41, 78]

        for studentID in self.getInput.get_student_dict():
            if studentID not in self.last_student_id and len(self.last_student_id) <= 7:
                self.screen.addstr(self.row1, pos[0], f"{self.getInput.get_student_dict()[studentID].get_student_id()}")
                self.screen.addstr(self.row1, pos[1], f"{self.getInput.get_student_dict()[studentID].get_name()}")
                self.screen.addstr(self.row1, pos[2], f"{self.getInput.get_student_dict()[studentID].get_dob()}")
                self.row1 += 1
                self.last_student_id.append(studentID)

        curses.noecho()

    # Display course information on the screen
    def display_course_info(self):
        self.getInput.get_course_info()

        for courseID in self.getInput.get_course_dict():
            if courseID not in self.last_course_id and len(self.last_course_id) <= 8:
                self.screen.addstr(self.row2, 0, f"{self.getInput.get_course_dict()[courseID].get_course_id()} - "
                                                 f"{self.getInput.get_course_dict()[courseID].get_name()} - "
                                                 f"{self.getInput.get_course_dict()[courseID].get_credits()}")
                self.row2 += 1
                self.last_course_id.append(courseID)

        curses.noecho()

    # Display mark on the screen
    def display_mark(self):
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.echo()

        # Get user's input for courseID and check if it's in courseDict
        self.screen.addstr(23, 33, "                                                            ")
        self.screen.addstr(23, 33, ">> Enter the courseID: ")
        row, col = self.screen.getyx()

        courseID = self.screen.getstr(row, col).decode("utf-8")
        if courseID not in self.getInput.get_course_dict():
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid courseID!")
            return

        for studentID in self.getInput.get_student_dict():
            if studentID in self.getInput.get_mark_dict() and courseID in self.getInput.get_mark_dict()[studentID]:
                array = self.getInput.get_mark_dict()[studentID][courseID]
                self.screen.addstr(self.row3, 89, "                               ")
                list(map(lambda col, element: self.screen.addstr(self.row3, 89 + 7 * col, str(element)),
                         range(len(array)), array))
            else:
                self.screen.addstr(self.row3, 89, "                               ")
                self.screen.addstr(self.row3, 89, "N/A")
            self.row3 += 1
        self.row3 = 12

        curses.noecho()

    # Calculate GPA for a specific student
    def calculate_gpa(self):
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.echo()

        # Get user's input for studentID
        self.screen.addstr(23, 33, "                                                            ")
        self.screen.addstr(23, 33, ">> Enter the studentID: ")
        row, col = self.screen.getyx()
        studentID = self.screen.getstr(row, col).decode("utf-8")

        # Calculate GPA
        average = 0
        total_credits = 0
        if studentID in self.getInput.get_mark_dict():
            for courseID in self.getInput.get_mark_dict()[studentID]:
                average += (self.getInput.get_mark_dict()[studentID][courseID][3] * self.getInput.get_course_dict()[courseID].get_credits())
                total_credits += self.getInput.get_course_dict()[courseID].get_credits()
            self.getInput.get_gpa_dict()[studentID] = math.floor((average / total_credits) * 10) / 10
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, f"Successfully calculate GPA for {self.getInput.get_student_dict()[studentID].get_name()}!")
        elif studentID in self.getInput.get_student_dict() and studentID not in self.getInput.get_mark_dict():
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, f">> {self.getInput.get_student_dict()[studentID].get_name()} doesn't have any marks yet!")
        else:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid studentID!")

        curses.noecho()

    # Sort GPA
    def sort_gpa(self):
        if not self.getInput.get_gpa_dict():
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, "There's not any GPAs yet!")
        else:
            sorted_GPA = sorted(self.getInput.get_gpa_dict().items(), key=lambda x: x[1], reverse=True)
            self.screen.addstr(23, 33, "                                                            ")
            for idx, dict in enumerate(sorted_GPA):
                self.screen.addstr(23 + idx, 33, f"#{idx + 1} {self.getInput.get_student_dict()[dict[0]].get_name()}: {dict[1]}")

    # Control the options for functions by using arrow key to change options and "enter" key to choose functions
    def run_opts(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        current_row_idx = 0
        self.print_opts(current_row_idx)

        while True:
            key = self.screen.getch()

            if key == curses.KEY_UP and current_row_idx > 0:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN and current_row_idx < len(self.menu) - 1:
                current_row_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.screen.addstr(1, 0, "[!]")
                self.screen.addstr(1, 4, "You pressed {}".format(self.menu[current_row_idx]))

                if self.menu[current_row_idx] == "Add Students":
                    self.display_student_info()
                elif self.menu[current_row_idx] == "Add Courses":
                    self.display_course_info()
                elif self.menu[current_row_idx] == "Add Marks":
                    self.getInput.get_mark_info()
                elif self.menu[current_row_idx] == "Display Marks":
                    self.display_mark()
                elif self.menu[current_row_idx] == "Calculate GPA":
                    self.calculate_gpa()
                elif self.menu[current_row_idx] == "Sort GPA":
                    self.sort_gpa()

                self.screen.refresh()
                self.screen.getch()

                if current_row_idx == len(self.menu) - 1:
                    break

            self.screen.addstr(1, 4, "                                        ")
            self.print_opts(current_row_idx)

    def main_func(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

        self.screen.clear()
        self.screen.refresh()

        self.draw_table()

        self.run_opts()

        self.screen.getch()
