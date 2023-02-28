import re

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
    def __init__(self, courseID, name):
        self.__courseID = courseID
        self.__name = name

    def getCourseID(self):
        return self.__courseID

    def getName(self):
        return self.__name

class Mark:
    def __init__(self, mark):
        self.__mark = mark

    def getMark(self):
        return self.__mark

class Major:
    def __init__(self):
        self.__studentDict = {}
        self.__courseDict = {}
        self.__markDict = {}

    def getStudentDict(self):
        return self.__studentDict
    
    def getCourseDict(self):
        return self.__courseDict

    def getMarkDict(self):
        return self.__markDict

    # Check the value whether it's valid or not

    def checkValue(self, num):
        try:
            num = int(num)
        except ValueError:
            print("Only integers are allowed!\n")
            return
        if (num >= 0):
            return int(num)
        else:
            print("You should enter a positive number!\n")

    # Input number of students in a class

    def studentNum(self):
        while True:
            studentNum = input("Enter number of students in a class: ")
            if self.checkValue(studentNum):
                return int(studentNum)
        
    # Input number of courses

    def courseNum(self):
        while True:
            courseNum = input("Enter number of courses: ")
            if self.checkValue(courseNum):
                return int(courseNum)

    # Input student information: id, name, DoB

    def studentInfo(self):
        id_pattern_1 = r"^BI\d{2}-\d{3}$"
        id_pattern_2 = r"^BA\d{2}-\d{3}$"
        print("")
        numOfStudents = self.studentNum()
        for i in range(numOfStudents):
            while True:
                id = input("Enter studentID (E.g: BIxx-xxx or BAxx-xxx): ")

                if re.match(id_pattern_1, id) or re.match(id_pattern_2, id):
                    break
                else:
                    print("Invalid ID format. Please try again.\n")

            name = input("Enter student name: ")
            dob = input("Enter student dob: ")
            self.__studentDict[id] = Student(id, name, dob)
            print("")

    # Input course information: id, name

    def courseInfo(self):
        print("")
        id_pattern = r"^ICT-\d{3}$"
        numOfCourses = self.courseNum()
        for i in range(numOfCourses):
            while True:
                id = input("Enter courseID (E.g: ICT-xxx): ")

                if re.match(id_pattern, id):
                    break
                else:
                    print("Invalid ID format. Please try again.\n")
            
            name = input("Enter course name: ")
            self.__courseDict[id] = Course(id, name)
            print("")

    # Select a course, input marks for student in this course

    def mark(self):
        courseID = input("Enter the courseID: ")
        if courseID not in self.__courseDict:
            print("Invalid courseID!")
            return
        for studentID in self.__studentDict:
            mark = float(input(f"Enter the mark for {self.__studentDict[studentID].getName()}: "))
            print("")
            if studentID not in self.__markDict:
                self.__markDict[studentID] = {}
            self.__markDict[studentID][courseID] = mark

    # List courses

    def courseList(self, courseID):
        print(f"{courseID}: {self.__courseDict[courseID].getName()}")
            
    # List students

    def studentList(self, studentID):
        print(f"+) {studentID}: {self.__studentDict[studentID].getName()}")
        
    # Show student marks for a given course

    def displayMark(self):
        print("")
        courseID = input("Enter the courseID: ")
        print("")
        if courseID not in self.__courseDict:
            print("Invalid courseID!")
            return
        for studentID in self.__studentDict:
            if studentID in self.__markDict and courseID in self.__markDict[studentID]:
                print(f"{self.__studentDict[studentID].getName()}: {self.__markDict[studentID][courseID]}")
            else:
                print(f"{self.__studentDict[studentID].getName()}: N/A")

    # Show everything including students and courses

    def allCourse(self):
        for courseID in self.__courseDict:
            print("")
            self.courseList(courseID)
            for studentID in self.__studentDict:
                self.studentList(studentID)
        print("")



major = Major()
major.studentInfo()
major.courseInfo()

while True:
    print("Pick an option: ")
    print("1. Input marks for a course")
    print("2. Display all course")
    print("3. Display mark list")
    print("4. Quit")
    print("")

    selection = int(input("Enter your choice: "))
    if selection == 1:
        major.mark()
    elif selection == 2:
        major.allCourse()
    elif selection == 3:
        major.displayMark()
    elif selection == 4:
        break
    else:
        print("")
        print("Invalid selection!")