import unittest
import datetime
from Student_Repository_Kavish_Sanghvi import main


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
            self.assertEqual(
                self.university_data.student['10103'].remaining_required, [
                    'SSW 540', 'SSW 555'], f'Invalid output.')
            print(f'Test Case 2. Test Case Passed')
        except AssertionError as e:
            print('Error: Test case 2 failed: ', e)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
