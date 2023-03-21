import gzip
import os.path
import re
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
            "───────────────────────────────│   ID   │                 Name               │   DOBs   │───────────────────────────────",
        ]

        for idx, row in enumerate(text):
            self.screen.addstr(idx, 0, row)

        for i in range(start, end + 1):
            self.screen.addstr(i, 0, "                               │        │                                    │          │                               ")
        self.screen.addstr(end, 0, "                               └────────────────────────────────────────────────────────┘                               ")

        self.screen.addstr(22, 0, "────────── Functions ───────────────────────────────────────────────────────────────────────────────────────────────────")
        for i in range(23, 29):
            self.screen.addstr(i, 0, "                               │                                                                                        ")

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

    # Display course information on the screen
    def get_course_info(self):
        self.getInput.get_course_info()

        for courseID in self.getInput.get_course_dict():
            if courseID not in self.last_course_id and len(self.last_course_id) <= 8:
                self.screen.addstr(self.row2, 0, f"{self.getInput.get_course_dict()[courseID].get_course_id()} - "
                                                 f"{self.getInput.get_course_dict()[courseID].get_name()} - "
                                                 f"{self.getInput.get_course_dict()[courseID].get_credits()}")
                self.row2 += 1
                self.last_course_id.append(courseID)

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
                list(map(lambda col, element: self.screen.addstr(self.row3, 89 + 7 * col, str(element)), range(len(array)), array))
                # self.screen.addstr(self.row3, 89, f"{self.__markDict[studentID][courseID]}")
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

    # Functions to compress files
    def compress_files(self, file1, file2, file3, dat_file):
        with gzip.open(dat_file, 'wb') as f:
            with open(file1, 'rb') as f1:
                f.write(f1.read())
            with open(file2, 'rb') as f2:
                f.write(f2.read())
            with open(file3, 'rb') as f3:
                f.write(f3.read())

    # Functions to decompress files
    def decompress_files(self, dat_file, file1, file2, file3):
        # Check if students.txt, courses.txt and marks.txt exists or not. If not, then create new

        for output_file in [file1, file2, file3]:
            if not os.path.exists(output_file):
                with open(output_file, 'w'):
                    pass

        # Split into 3 files based on their format
        if os.path.exists(dat_file):
            with gzip.open(dat_file, 'rb') as f:
                for line in f:
                    line_str = line.decode("utf-8")

                    # students.txt saved with format BIxx-xxx - Name - Dob
                    if re.match(r"^BI\d{2}-\d{3}$", line_str[0:8]):
                        with open(file1, 'a') as f1, open(file1, 'r') as f1_read:
                            if line_str[0:8] not in f1_read.read():
                                f1.write(f"{line_str}")

                    # courses.txt saved with format ICT-xxx - Name - Credits
                    elif re.match(r"^ICT-\d{3}$", line_str[0:7]):
                        with open(file2, 'a') as f2, open(file2, 'r') as f2_read:
                            if line_str[0:7] not in f2_read.read():
                                f2.write(line_str)

                    # Others
                    else:
                        with open(file3, 'a') as f3, open(file3, 'r') as f3_read:
                            if line_str not in f3_read.read():
                                   f3.write(line_str)
        else:
            return

    # load data from txt files
    def load_data(self, file1, file2, file3):
        # students.txt saved with format BIxx-xxx - Name - Dob
        with open(file1, 'r') as f1:
            for line in f1:
                if line == "\n":
                    continue
                line = line.replace(" - ", "")
                self.getInput.get_student_dict()[line[0:8]] = Student(line[0:8], line[8:-11], line[-11:-1])
                self.getInput.get_mark_dict()[line[0:8]] = {}

        # courses.txt saved with format ICT-xxx - Name - Credits
        with open(file2, 'r') as f2:
            for line in f2:
                if line == "\n":
                    continue
                line = line.replace(" - ", "")
                self.getInput.get_course_dict()[line[0:7]] = Course(line[0:7], line[7:-2], int(line[-2:-1]))

        # marks.txt saved with format # ICT-xxx - BIxx-xxx - Name - Mark
        with open(file3, 'r') as f3:
            for line in f3:
                if line == "\n":
                    continue
                line = line.replace(" - ", "")
                self.getInput.get_mark_dict()[line[7:15]][line[0:7]] = np.array([line[15:19], line[21:25], line[27:31], line[33:37]])

    # Control the options for functions by using arrow key to change options and "enter" key to choose functions
    def run_func(self):
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
                    self.get_course_info()
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

        self.decompress_files("students.dat", "students.txt", "courses.txt", "marks.txt")
        self.draw_table()
        self.load_data("students.txt", "courses.txt", "marks.txt")

        self.run_func()
        self.compress_files("students.txt", "courses.txt", "marks.txt", "students.dat")

        self.screen.getch()
