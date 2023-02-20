# ~~~~~~~~~~~~~~~~~~~~ INPUT FUNCTIONS ~~~~~~~~~~~~~~~~~~~~

studentDict = {}
courseDict = {}
markDict = {}

# Input number of students in a class

def studentNum():
    return int(input("Enter number of students in a class: "))

# Input number of courses

def courseNum():
    return int(input("Enter number of courses: "))

# Input student information: id, name, DoB

def studentInfo():
    print("")
    numOfStudents = studentNum()
    print("")
    for i in range(numOfStudents):
        id = input("Enter studentID: ")
        name = input("Enter student name: ")
        dob = input("Enter student dob: ")
        studentDict[id] = {"name": name, "dob": dob}
        print("")

# Input course information: id, name

def courseInfo():
    print("")
    numOfCourses = courseNum()
    print("")
    for i in range(numOfCourses):
        id = input("Enter courseID: ")
        name = input("Enter course name: ")
        courseDict[id] = {"name": name}
        print("")

# Select a course, input marks for student in this course

def mark():
    courseID = input("Enter the courseID: ")
    if courseID not in courseDict:
        print("Invalid courseID!")
        return
    for studentID in studentDict:
        mark = float(input(f"Enter the mark for {studentDict[studentID]['name']}: "))
        print("")
        if studentID not in markDict:
            markDict[studentID] = {}
        markDict[studentID][courseID] = mark

# ~~~~~~~~~~~~~~~~~~~~ LISTING FUNCTIONS ~~~~~~~~~~~~~~~~~~~~

# List courses

def courseList(courseID):
    print(f"{courseID}: {courseDict[courseID]['name']}")
        

# List students

def studentList(studentID):
    print(f"+) {studentID}: {studentDict[studentID]['name']}")
    
# Show student marks for a given course

def displayMark():
    print("")
    courseID = input("Enter the courseID: ")
    print("")
    if courseID not in courseDict:
        print("Invalid courseID!")
        return
    for studentID in studentDict:
        if studentID in markDict and courseID in markDict[studentID]:
            
            print(f"{studentDict[studentID]['name']}: {markDict[studentID][courseID]}")
        else:
            print(f"{studentDict[studentID]['name']}: N/A")

# Show everything including students and courses

def allCourse():
    for courseID in courseDict:
        print("")
        courseList(courseID)
        for studentID in studentDict:
            studentList(studentID)
    print("")

# ~~~~~~~~~~~~~~~~~~~~ MAIN FUNCTIONS ~~~~~~~~~~~~~~~~~~~~

studentInfo()
courseInfo()

print("")

while True:
    print("Pick an option: ")
    print("1. Input marks for a course")
    print("2. Display all course")
    print("3. Display mark list")
    print("4. Quit")
    print("")

    selection = int(input("Enter your choice: "))
    if selection == 1:
        mark()
    elif selection == 2:
        allCourse()
    elif selection == 3:
        displayMark()
    elif selection == 4:
        break
    else:
        print("")
        print("Invalid selection!")





