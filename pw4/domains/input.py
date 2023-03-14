import curses
import math
import numpy as np


class Student:
    def __init__(self, studentID, name, dob):
        self.__studentID = studentID
        self.__name = name
        self.__dob = dob

    def getStudentID(self):
        return self.__studentID

    def getName(self):
        return self.__name

    def getDob(self):
        return self.__dob


class Course:
    def __init__(self, courseID, name, credits):
        self.__courseID = courseID
        self.__name = name
        self.__credits = credits

    def getCourseID(self):
        return self.__courseID

    def getName(self):
        return self.__name

    def getCredits(self):
        return self.__credits


class Input:
    def __init__(self):
        self.__studentDict = {}
        self.__courseDict = {}
        self.__markDict = {}
        self.__gpaDict = {}
        self.menu = ['Add Students', 'Add Courses', 'Add Marks', 'Display Marks', 'Calculate GPA', 'Sort GPA',
                     'Exit']
        self.screen = curses.initscr()

    def getStudentDict(self):
        return self.__studentDict

    def getCourseDict(self):
        return self.__courseDict

    def getMarkDict(self):
        return self.__markDict

    def getGpaDict(self):
        return self.__gpaDict

    def studentInfo(self, studentNum=2):
        curses.curs_set(0)

        self.screen.keypad(True)
        curses.echo()

        pos = [32, 41, 78]
        commands = [">> Enter studentID (E.g: BIxx-xxx or BAxx-xxx): ",
                    ">> Enter student name: ",
                    ">> Enter student dob: "]

        a = []
        for i in range(studentNum):
            for j in commands:
                self.screen.addstr(23, 33, "                                                            ")
                self.screen.addstr(23, 33, j)
                row, col = self.screen.getyx()

                user_input = self.screen.getstr(row, col).decode()
                a.append(user_input)

            self.__studentDict[a[0]] = Student(a[0], a[1], a[2])
            a = []

    def courseInfo(self, courseNum=2):
        curses.curs_set(0)

        self.screen.keypad(True)
        curses.echo()

        commands = [">> Enter courseID (E.g: ICT-xxx): ",
                    ">> Enter course name: ",
                    ">> Enter the credits of the course: "]

        a = []
        for i in range(courseNum):
            for j in commands:
                self.screen.addstr(23, 33, "                                                            ")
                self.screen.addstr(23, 33, j)
                row, col = self.screen.getyx()

                user_input = self.screen.getstr(row, col).decode("utf-8")
                a.append(user_input)

            self.__courseDict[a[0]] = Course(a[0], a[1], int(a[2]))
            a = []

    def markInfo(self):
        curses.curs_set(0)

        self.screen.keypad(True)
        curses.echo()

        commands = [">> Enter the attendance mark for ",
                    ">> Enter the midterm mark for ",
                    ">> Enter the final mark for "]

        self.screen.addstr(23, 33, "                                                            ")
        self.screen.addstr(23, 33, ">> Enter the courseID: ")
        row, col = self.screen.getyx()

        courseID = self.screen.getstr(row, col).decode("utf-8")
        if courseID not in self.__courseDict:
            self.screen.addstr(23, 33, "                                                            ")
            self.screen.addstr(23, 33, ">> Invalid courseID!")
            return

        a = []
        for studentID in self.__studentDict:
            for j in commands:
                self.screen.addstr(23, 33, "                                                            ")
                self.screen.addstr(23, 33, f"{j}{self.__studentDict[studentID].getName()}: ")
                row, col = self.screen.getyx()

                user_input = self.screen.getstr(row, col).decode("utf-8")
                a.append(math.floor(float(user_input) * 10) / 10)
            a.append(math.floor(float(a[0] * 0.1 + a[1] * 0.4 + a[2] * 0.5) * 10) / 10)

            if studentID not in self.__markDict:
                self.__markDict[studentID] = {}
            self.__markDict[studentID][courseID] = np.array([a[0], a[1], a[2], a[3]])
            a = []

        curses.noecho()

