from HW08_Kavish_Sanghvi import file_reader
from prettytable import PrettyTable
import os
import sqlite3


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
        self.cgpa: float = 0
        self.completed_courses = []
        self.remaining_required = []
        self.remaining_electives = []


class Instructor:
    def __init__(self, cwid, name, dept, courses) -> None:
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


class Majors:
    def __init__(self, major, required_courses, electives):
        ''' stores the majors information

        :param major: major name
        :type major: string

        :param required_courses: list of required courses for that major
        :type required_courses: list

        :param electives: list of the electives for a major
        :type electives: list

        :rtype: None
        :return: None
        '''
        self.major = major
        self.required_courses = required_courses
        self.electives = electives


class University:
    def __init__(self, name, student, instructor, major, path):
        ''' stores the univeristy data

        :param student: contains a each student and its details
        :type student: dict

        :param instructor: stores each instructor and its details
        :type name: string

        :param major: stores each major and its details
        :type major: string

        :param path: path for the grades file
        :type path: string


        :rtype: None
        :return: None
        '''

        self.name: str = name
        self.student: dict = student
        self.instructor: dict = instructor
        self.major: dict = major
        self.path = path
        self.process_all_data()
        self.calculate_cgpa()


    def process_all_data(self):
        grades = file_reader(self.path + 'grades.txt', 4, '\t', header=True)
        
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
            if grade not in ['D+', 'D', 'D-', 'F']:
                student.completed_courses.append(course_name)

            instructor = self.instructor[instructor_cwid]

            if instructor.courses.get(course_name):
                instructor.courses[course_name] += 1
            else:
                instructor.courses[course_name] = 1

            student.remaining_required = list(
                set(self.major[student.major].required_courses) - set(student.completed_courses))
            flag = False
            for ele in student.completed_courses:
                if ele in self.major[student.major].electives:
                    flag = True
                    break
            if flag:
                student.remaining_electives = []
            else:
                student.remaining_electives = list(
                    set(self.major[student.major].electives) - set(student.completed_courses))

    def get_grade_value(self, grade) -> float:
        grades_dict = {
            'A': 4.0,
            'A-': 3.75,
            'B+': 3.25,
            'B': 3.0,
            'B-': 2.75,
            'C+': 2.25,
            'C': 2.0,
            'C-': 0,
            'D+': 0,
            'D': 0,
            'D-': 0,
            'F': 0}
        return grades_dict[grade]

    def calculate_cgpa(self) -> None:
        students_info = self.student
        for cwid, value in students_info.items():
            total = 0
            for courses, grade in value.courses.items():
                total += self.get_grade_value(grade)
            if len(list(value.courses.keys())) != 0:
                cgpa = total / len(list(value.courses.keys()))
                value.cgpa = round(cgpa, 2)
            else:
                value.cgpa = 0

    def student_grades_table_db(self, db_path) -> None:
        db_file: str = db_path
        db: sqlite3.Connection = sqlite3.connect(db_file)
        query: str = "select students.Name, grades.StudentCWID, grades.Course, grades.Grade, instructors.Name from grades \
                  JOIN students on grades.StudentCWID = students.CWID \
                  JOIN instructors on grades.InstructorCWID = instructors.CWID \
                  ORDER BY students.Name ASC"
        
        ans: list = []
        for row in db.execute(query):
            ans.append((row))
            
        db.commit()
        db.close()
        return ans
                
                       
    def display_and_save(self) -> None:
        ''' pretty print the data

        :param None
        :type None

        :rtype: None
        :return: None
        '''
        
        x = PrettyTable()
        x.field_names = [
            'CWID',
            'Name',
            'Major',
            'Completed Courses',
            'Remaining Required',
            'Remaining Electives',
            'GPA']
        for k, l in self.student.items():
            row = []
            values = [
                l.cwid, l.name, l.major, sorted(
                    l.completed_courses), sorted(
                    l.remaining_required), sorted(
                    l.remaining_electives), l.cgpa]
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

        z = PrettyTable()
        z.field_names = ['Major', 'Required Courses', 'Electives']
        
        for k, l in self.major.items():
            row = []
            values = [l.major, sorted(l.required_courses), sorted(l.electives)]
            row.extend(values)
            z.add_row(row)

        l = PrettyTable()
        l.field_names = ['Name', 'CWID', 'Course', 'Grade', 'Instructor']
        students_grade_summary = self.student_grades_table_db('lab11.db')
        for k in students_grade_summary:
            row = []
            values = [k[0], k[1], k[2], k[3], k[4]]
            row.extend(values)
            l.add_row(row)

            
        print('Students Summary')
        print(x)
        print()
        
        print('Instructor Summary')
        print(y)
        print()
        
        print('Majors Summary')
        print(z)
        print()

        print('Students Grade Summary')
        print(l)
        print()

        if not os.path.isdir(self.name):
            os.mkdir(self.name)
            os.chdir(self.name)

        x_data = x.get_string()

        with open('student_info.txt', 'w') as f:
            f.write(x_data)
            f.close()

        y_data = y.get_string()

        with open('instructor_info.txt', 'w') as f:
            f.write(y_data)
            f.close()


def main(uni_name, path=''):
    ''' main function that operates entire clases

        :optional param path: path to the directory of data files or default is ''
        :type path: string


        :return: None
    '''
    students_info: dict = {}

    students = file_reader(path + 'students.txt', 3, '\t', header=True)

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

    instructors = file_reader(path + 'instructors.txt', 3, '\t', header=True)

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

    majors = file_reader(path + 'majors.txt', 3, '\t', header=True)
    majors_dict: dict = {}

    for line in majors:

        try:
            if len(line[0]) < 1:
                raise 'Invalid data entry found'
            if len(line[1]) < 1:
                raise 'Invalid data entry found'
            if len(line[2]) < 1:
                raise 'Invalid data entry found'
        except BaseException:
            continue

        major_name = line[0]
        r_or_e = line[1]
        course = line[2]
        r_flag = False

        if r_or_e == 'R':
            r_flag = True
        else:
            r_flag = False

        if majors_dict.get(major_name):
            if r_flag:
                majors_dict[major_name]['required_courses'].append(course)
            else:
                majors_dict[major_name]['electives'].append(course)
        else:
            majors_dict[major_name] = {}
            majors_dict[major_name]['required_courses'] = []
            majors_dict[major_name]['electives'] = []
            if r_flag:
                majors_dict[major_name]['required_courses'] = [course]
            else:
                majors_dict[major_name]['electives'] = [course]

    major_info: dict = {}
    for major, info in majors_dict.items():
        major_obj = Majors(
            major,
            majors_dict[major]['required_courses'],
            majors_dict[major]['electives'])
        major_info[major] = major_obj

    university_data = University(
        uni_name,
        students_info,
        instructors_info,
        major_info,
        path)
    university_data.display_and_save()

    return university_data
