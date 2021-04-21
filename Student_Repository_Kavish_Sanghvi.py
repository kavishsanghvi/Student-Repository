from HW08_Kavish_Sanghvi import file_reader
from prettytable import PrettyTable
import os


class Student:
    def __init__(self, cwid, name, major, courses):
        ''' stores the student data

        :param cwid: stores the student cwid
        :type cwid: string

        :param name: stores the student name
        :type name: string

        :param major: stores the student major
        :type name: string

        :param courses: stores the student course and its grade in a dict
        :type name: dict

        :rtype: None
        :return: None
        '''

        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: dict = courses


class Instructor:
    def __init__(self, cwid, name, dept, courses):
        ''' stores the instructor data

        :param cwid: stores the instructor cwid
        :type cwid: string

        :param name: stores the instructor name
        :type name: string

        :param dept: stores the instructor dept
        :type dept: string

        :param courses: stores the instructor courses and its no of students in each course in a dict
        :type name: dict

        :rtype: None
        :return: None
        '''

        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: dict = courses


class University:
    def __init__(self, name, student, instructor, path):
        ''' stores the univeristy data

        :param ntains a each student and its details
        :type student: dict

        :param instructor: stores each instructor and its details
        :type name: string

        :param path: path for the grades file
        :type path: string

        :rtype: None
        :return: None
        '''

        self.name: str = name
        self.student: dict = student
        self.instructor: dict = instructor
        self.path = path
        self.process_all_data()

    def process_all_data(self):
        grades = file_reader(self.path + 'grades.txt', 4, '\t')

        for line in grades:
            try:
                if len(line[0]) < 1:
                    raise 'Invalid data entry found'
                if len(line[1]) < 1:
                    raise 'Invalid data entry found'
                if len(line[2]) < 1:
                    raise 'Invalid data entry found'
                if len(line[3]) < 1:
                    raise 'Invalid data entry found'
            except BaseException:
                continue

            student_cwid = line[0]
            course_name = line[1]
            grade = line[2]
            instructor_cwid = line[3]
            student = self.student[student_cwid]
            student.courses[course_name] = grade
            instructor = self.instructor[instructor_cwid]

            if instructor.courses.get(course_name):
                instructor.courses[course_name] += 1
            else:
                instructor.courses[course_name] = 1

    def display_and_save(self) -> None:
        ''' pretty print the data

        :param None
        :type None

        :rtype: None
        :return: None
        '''

        x = PrettyTable()
        x.field_names = ['CWID', 'Name', 'Courses']
        for k, l in self.student.items():
            row = []
            values = [l.cwid, l.name, sorted(list(l.courses.keys()))]
            row.extend(values)
            x.add_row(row)

        y = PrettyTable()
        y.field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']

        for k, l in self.instructor.items():
            for course, grade in l.courses.items():
                row = []
                values = [l.cwid, l.name, l.dept, course, grade]
                row.extend(values)
                y.add_row(row)

        print(x)
        print(y)

        if not os.path.isdir(self.name):
            os.mkdir(self.name)
            os.chdir(self.name)
        x_data = x.get_string()

        with open('student_info.txt', 'w') as f:
            f.write(x_data)
        y_data = y.get_string()

        with open('instructor_info.txt', 'w') as f:
            f.write(y_data)


def main(uni_name, path=''):
    ''' main function that operates entire clases

        :optional param path: path to the directory of data files or default is ''
        :type path: string


        :return: None
    '''

    students_info: dict = {}
    students = file_reader(path + 'students.txt', 3, '\t')

    for line in students:
        try:
            if len(line[0]) < 1:
                raise 'Invalid data entry found'
            if len(line[1]) < 1:
                raise 'Invalid data entry found'
            if len(line[2]) < 1:
                raise 'Invalid data entry found'
        except BaseException:
            continue

        student = Student(line[0], line[1], line[2], {})
        students_info[line[0]] = student

    instructors_info: dict = {}
    instructors = file_reader(path + 'instructors.txt', 3, '\t')

    for line in instructors:

        try:
            if len(line[0]) < 1:
                raise 'Invalid data entry found'
            if len(line[1]) < 1:
                raise 'Invalid data entry found'
            if len(line[2]) < 1:
                raise 'Invalid data entry found'
        except BaseException:
            continue

        instructor = Instructor(line[0], line[1], line[2], {})
        instructors_info[line[0]] = instructor

    university_data = University(
        uni_name,
        students_info,
        instructors_info,
        path)
    university_data.display_and_save()

    return university_data
