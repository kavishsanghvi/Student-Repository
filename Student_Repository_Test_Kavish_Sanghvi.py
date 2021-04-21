import unittest
import datetime
from HW09_Kavish_Sanghvi import main


class TestMainFunction(unittest.TestCase):
    def data(self):
        # Note path is optional parameter so by default it passes ''
        self.university_data = main('Stevens University')

    def test_student_name(self):
        """ Test if the student name is correct

        param: None
        returns: None
        """

        self.data()

        try:
            self.assertEqual(
                self.university_data.student['10103'].name,
                'Baldwin, C',
                f'Invalid output. The correct output should be Baldwin, C')
            print(f'Test Case 1. Test Case Passed')
        except AssertionError as e:
            print('Error: Test case 1 failed: ', e)

    def test_student_courses(self):
        """ Test if the student name is correct

        param: None
        returns: None
        """

        self.data()

        try:
            self.assertEqual(list(self.university_data.student['10103'].courses.keys()), [
                             'SSW 567', 'SSW 564', 'SSW 687', 'CS 501'], f'Invalid output.')
            print(f'Test Case 2. Test Case Passed')
        except AssertionError as e:
            print('Error: Test case 2 failed: ', e)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
