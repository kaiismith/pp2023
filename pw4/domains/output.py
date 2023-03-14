from input import *


class Output:
    def __init__(self):
        self.row1 = 12
        self.row2 = 12
        self.row3 = 12
        self.lastStudentID = []
        self.lastCourseID = []
        self.lastMark = []
        self.menu = ['Add Students', 'Add Courses', 'Add Marks', 'Display Marks', 'Calculate GPA', 'Sort GPA', 'Exit']
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

    def print_func(self, selected_row_idx):
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

    def get_studentInfo(self):
        self.getInput.studentInfo()

        pos = [32, 41, 78]
        for studentID in self.getInput.getStudentDict():
            if studentID not in self.lastStudentID and len(self.lastStudentID) <= 7:
                self.screen.addstr(self.row1, pos[0], f"{self.getInput.getStudentDict()[studentID].getStudentID()}")
                self.screen.addstr(self.row1, pos[1], f"{self.getInput.getStudentDict()[studentID].getName()}")
                self.screen.addstr(self.row1, pos[2], f"{self.getInput.getStudentDict()[studentID].getDob()}")
                self.row1 += 1
                self.lastStudentID.append(studentID)

        curses.noecho()

    def get_courseInfo(self):
        self.getInput.courseInfo()

        for courseID in self.getInput.getCourseDict():
            if courseID not in self.lastCourseID and len(self.lastCourseID) <= 8:
                self.screen.addstr(self.row2, 0, f"{self.getInput.getCourseDict()[courseID].getCourseID()} - "
                                                 f"{self.getInput.getCourseDict()[courseID].getName()} - "
                                                 f"{self.getInput.getCourseDict()[courseID].getCredits()}")
                self.row2 += 1
                self.lastCourseID.append(courseID)

        curses.noecho()

    def displayMark(self):
        curses.curs_set(0)

        self.screen.keypad(True)
        curses.echo()

        self.screen.addstr(23, 33, "                                                            ")
        self.screen.addstr(23, 33, ">> Enter the courseID: ")
        row, col = self.screen.getyx()

        courseID = self.screen.getstr(row, col).decode("utf-8")
        if courseID not in self.getInput.getCourseDict():
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid courseID!")
            return

        for studentID in self.getInput.getStudentDict():
            if studentID in self.getInput.getMarkDict() and courseID in self.getInput.getMarkDict()[studentID]:
                array = self.getInput.getMarkDict()[studentID][courseID]
                self.screen.addstr(self.row3, 89, "                               ")
                list(map(lambda col, element: self.screen.addstr(self.row3, 89 + 7 * col, str(element)),
                         range(len(array)), array))
            else:
                self.screen.addstr(self.row3, 89, "                               ")
                self.screen.addstr(self.row3, 89, "N/A")
            self.row3 += 1
        self.row3 = 12

    def calculateGPA(self):
        curses.curs_set(0)

        self.screen.keypad(True)
        curses.echo()

        self.screen.addstr(23, 33, "                                                            ")
        self.screen.addstr(23, 33, ">> Enter the studentID: ")
        row, col = self.screen.getyx()

        studentID = self.screen.getstr(row, col).decode("utf-8")
        average = 0
        total_credits = 0
        if studentID in self.getInput.getMarkDict():
            for courseID in self.getInput.getMarkDict()[studentID]:
                average += (self.getInput.getMarkDict()[studentID][courseID][3] * self.getInput.getCourseDict()[courseID].getCredits())
                total_credits += self.getInput.getCourseDict()[courseID].getCredits()
            self.getInput.getGpaDict()[studentID] = math.floor((average / total_credits) * 10) / 10
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, f"Successfully calculate GPA for {self.getInput.getStudentDict()[studentID].getName()}!")
        elif studentID in self.getInput.getStudentDict() and studentID not in self.getInput.getMarkDict():
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, f">> {self.getInput.getStudentDict()[studentID].getName()} doesn't have any marks yet!")
        else:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid studentID!")

    def sortGPA(self):
        if not self.getInput.getGpaDict():
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, "There's not any GPAs yet!")
        else:
            sorted_GPA = sorted(self.getInput.getGpaDict().items(), key=lambda x: x[1], reverse=True)
            self.screen.addstr(23, 33, "                                                            ")
            for idx, dict in enumerate(sorted_GPA):
                self.screen.addstr(23 + idx, 33, f"#{idx + 1} {self.getInput.getStudentDict()[dict[0]].getName()}: {dict[1]}")

    def run_func(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        current_row_idx = 0
        pos = [32, 41, 78]

        self.print_func(current_row_idx)

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
                    self.get_studentInfo()
                elif self.menu[current_row_idx] == "Add Courses":
                    self.get_courseInfo()
                elif self.menu[current_row_idx] == "Add Marks":
                    self.getInput.markInfo()
                elif self.menu[current_row_idx] == "Display Marks":
                    self.displayMark()
                elif self.menu[current_row_idx] == "Calculate GPA":
                    self.calculateGPA()
                elif self.menu[current_row_idx] == "Sort GPA":
                    self.sortGPA()

                self.screen.refresh()
                self.screen.getch()

                if current_row_idx == len(self.menu) - 1:
                    break

            self.screen.addstr(1, 4, "                                        ")
            self.print_func(current_row_idx)

    def main_func(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

        self.screen.clear()
        self.screen.refresh()

        self.draw_table()

        self.run_func()

        self.screen.getch()





