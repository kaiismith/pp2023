import math
import numpy as np
import curses

# Class Student - private
class Student:
    def __init__(self, studentID, name, dob):
        self.__studentID = studentID
        self.__name = name
        self.__dob = dob

    def get_student_id(self):
        return self.__studentID

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

# Class Course - private
class Course:
    def __init__(self, courseID, name, credits):
        self.__courseID = courseID
        self.__name = name
        self.__credits = credits

    def get_course_id(self):
        return self.__courseID

    def get_name(self):
        return self.__name

    def get_credits(self):
        return self.__credits

# Class Major
class Major:
    def __init__(self):
        # Dictionaries that contain all the information about students, courses, marks and GPAs
        self.__student_dict = {}
        self.__course_dict = {}
        self.__mark_dict = {}
        self.__gpa_dict = {}

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
        self.screen = curses.initscr()

    def get_student_dict(self):
        return self.__student_dict

    def get_course_dict(self):
        return self.__course_dict

    def get_mark_dict(self):
        return self.__mark_dict

    def get_gpa_dict(self):
        return self.__gpa_dict

    # Initialize the table
    def draw_table(self):
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

        for i in range(12, 21):
            self.screen.addstr(i, 0, "                               │        │                                    │          │                               ")
        self.screen.addstr(20, 0, "                               └────────────────────────────────────────────────────────┘                               ")

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

    # Get user's input for student information (studentNum should be <= 8)
    def get_student_info(self, studentNum=2):
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.echo()

        # "pos" contains 3 positions (staring columns) to print after input ID, name, dob
        pos = [32, 41, 78]

        commands = [">> Enter studentID (E.g: BIxx-xxx or BAxx-xxx): ",
                    ">> Enter student name: ",
                    ">> Enter student dob (E.g: xx/xx/xxx): "]

        # Get the position right next to the text in "commands" to type from keyboard
        a = []
        for i in range(studentNum):
            for j in commands:
                self.screen.addstr(23, 33, "                                                            ")
                self.screen.addstr(23, 33, j)
                row, col = self.screen.getyx()
                user_input = self.screen.getstr(row, col).decode()
                a.append(user_input)

            self.__student_dict[a[0]] = Student(a[0], a[1], a[2])
            a = []

        for studentID in self.__student_dict:
            if studentID not in self.last_student_id and len(self.last_student_id) <= 8:
                self.screen.addstr(self.row1, pos[0], f"{self.__student_dict[studentID].get_student_id()}")
                self.screen.addstr(self.row1, pos[1], f"{self.__student_dict[studentID].get_name()}")
                self.screen.addstr(self.row1, pos[2], f"{self.__student_dict[studentID].get_dob()}")
                self.row1 += 1
                self.last_student_id.append(studentID)

        curses.noecho()

    # Get user's input for course information (courseNum should be <= 8)
    def get_course_info(self, courseNum=2):
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.echo()

        commands = [">> Enter courseID (E.g: ICT-xxx): ",
                    ">> Enter course name: ",
                    ">> Enter the credits of the course: "]

        # Get the position right next to the text in "commands" to type from keyboard
        a = []
        for i in range(courseNum):
            for j in commands:
                self.screen.addstr(23, 33, "                                                            ")
                self.screen.addstr(23, 33, j)
                row, col = self.screen.getyx()
                user_input = self.screen.getstr(row, col).decode("utf-8")
                a.append(user_input)

            self.__course_dict[a[0]] = Course(a[0], a[1], int(a[2]))
            a = []

        for courseID in self.__course_dict:
            if courseID not in self.last_course_id and len(self.last_course_id) <= 8:
                self.screen.addstr(self.row2, 0, f"{self.__course_dict[courseID].get_course_id()} - "
                                                 f"{self.__course_dict[courseID].get_name()} - "
                                                 f"{self.__course_dict[courseID].get_credits()}")
                self.row2 += 1
                self.last_course_id.append(courseID)

        curses.noecho()

    # Get user's input for mark of a specific course using courseID
    def get_mark_info(self):
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.echo()

        commands = [">> Enter the attendance mark for ",
                    ">> Enter the midterm mark for ",
                    ">> Enter the final mark for "]

        # Get user's input for courseID and check if it's in courseDict
        self.screen.addstr(23, 33, "                                                            ")
        self.screen.addstr(23, 33, ">> Enter the courseID: ")
        row, col = self.screen.getyx()
        courseID = self.screen.getstr(row, col).decode("utf-8")
        if courseID not in self.__course_dict:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid courseID!")
            return

        a = []
        for studentID in self.__student_dict:
            for j in commands:
                self.screen.addstr(23, 33, "                                                            ")
                self.screen.addstr(23, 33, f"{j}{self.__student_dict[studentID].get_name()}: ")
                row, col = self.screen.getyx()
                user_input = self.screen.getstr(row, col).decode("utf-8")

                # Using math.floor to round down to 1 decimal: math.floor(num * 10) / 10
                a.append(math.floor(float(user_input) * 10) / 10)
            # Calculate total mark
            a.append(math.floor(float(a[0] * 0.1 + a[1] * 0.4 + a[2] * 0.5) * 10) / 10)

            if studentID not in self.__mark_dict:
                self.__mark_dict[studentID] = {}

            # Using numpy to create array which contains attendance, midterm, final and total mark, respectively
            self.__mark_dict[studentID][courseID] = np.array([a[0], a[1], a[2], a[3]])
            a = []

        curses.noecho()

    # Display Mark
    def display_mark(self):
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.echo()

        # Get user's input for courseID and check if it's in courseDict
        self.screen.addstr(23, 33, "                                                            ")
        self.screen.addstr(23, 33, ">> Enter the courseID: ")
        row, col = self.screen.getyx()
        courseID = self.screen.getstr(row, col).decode("utf-8")
        if courseID not in self.__course_dict:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid courseID!")
            return

        for studentID in self.__student_dict:
            if studentID in self.__mark_dict and courseID in self.__mark_dict[studentID]:
                mark = self.__mark_dict[studentID][courseID]
                self.screen.addstr(self.row3, 89, "                               ")
                list(map(lambda col, element: self.screen.addstr(self.row3, 89 + 7 * col, str(element)), range(len(mark)), mark))

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
        if studentID in self.__mark_dict:
            for courseID in self.__mark_dict[studentID]:
                average += (self.__mark_dict[studentID][courseID][3] * self.__course_dict[courseID].get_credits())
                total_credits += self.__course_dict[courseID].get_credits()
            self.__gpa_dict[studentID] = math.floor((average / total_credits) * 10) / 10
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, f"Successfully calculate GPA for {self.__student_dict[studentID].get_name()}!")
        elif studentID in self.__student_dict and studentID not in self.__mark_dict:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, f">> {self.__student_dict[studentID].get_name()} doesn't have any marks yet!")
        else:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid studentID!")

        curses.noecho()

    # Sort GPA
    def sort_gpa(self):
        if not self.__gpa_dict:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, "There's not any GPAs yet!")
        else:
            sorted_GPA = sorted(self.__gpa_dict.items(), key=lambda x: x[1], reverse=True)
            for idx, dict in enumerate(sorted_GPA):
                self.screen.addstr(23, 33, f"#{idx + 1} {self.__student_dict[dict[0]].get_name()}: {dict[1]}")

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
                    self.get_student_info()
                elif self.menu[current_row_idx] == "Add Courses":
                    self.get_course_info()
                elif self.menu[current_row_idx] == "Add Marks":
                    self.get_mark_info()
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


def main(stdscr):
    major = Major()
    major.main_func()


curses.wrapper(main)

