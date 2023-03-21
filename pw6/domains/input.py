import curses
import math
import numpy as np
import os


# Class Student
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


# Class Course
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

# Class Input
class Input:
    def __init__(self):
        # Dictionaries that contain all the information about students, courses, marks and GPAs
        self.__student_dict = {}
        self.__course_dict = {}
        self.__mark_dict = {}
        self.__gpa_dict = {}

        self.screen = curses.initscr()

    def get_student_dict(self):
        return self.__student_dict

    def get_course_dict(self):
        return self.__course_dict

    def get_mark_dict(self):
        return self.__mark_dict

    def get_gpa_dict(self):
        return self.__gpa_dict

    # Write to files based on the ID of students and courses
    def write_to_file(self, filename, content):
        if os.path.exists(filename):
            with open(filename, 'a') as f, open(filename, 'r') as f_read:
                if filename == "students.txt":
                    if content[0:8] not in f_read.read():
                        f.write(content)
                elif filename == "courses.txt":
                    if content[0:7] not in f_read.read():
                        f.write(content)
                else:
                    if content not in f_read.read():
                        f.write(content)
        else:
            with open(filename, 'w') as f:
                f.write(content)

    # Get user's input for student information (studentNum should be <= 8)
    def get_student_info(self, studentNum=2):
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.echo()

        commands = [">> Enter studentID (E.g: BIxx-xxx or BAxx-xxx): ",
                    ">> Enter student name: ",
                    ">> Enter student dob: "]

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
            self.write_to_file("students.txt", f"{a[0]} - {a[1]} - {a[2]}\n")
            a = []

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
            self.write_to_file("courses.txt", f"{a[0]} - {a[1]} - {a[2]}\n")
            a = []

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
            self.write_to_file("marks.txt", f"#{courseID} - {self.__student_dict[studentID].get_student_id()} - {a[0]}  {a[1]}  {a[2]}  {a[3]}\n")
            a = []

        curses.noecho()
