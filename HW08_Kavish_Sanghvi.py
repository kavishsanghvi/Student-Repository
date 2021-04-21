from datetime import timedelta
from datetime import datetime
from typing import List, Any, Tuple, Iterator, Dict
from datetime import date
import os
from prettytable import PrettyTable


# PART 1

def date_arithmetic() -> Tuple[datetime, datetime, int]:
    ''' returns tuple in the (datetime, datetime, int) format

        :param None
        :type None

        :rtype: Tuple
        :return: Tuple[datetime, datetime, int]
    '''

    three_days_after_02272020: datetime = datetime(2020, 2, 27)
    three_days_after_02272019: datetime = datetime(2019, 2, 27)
    days_passed_02012019_09302019: int = 0

    three_days_after_02272020 = three_days_after_02272020 + timedelta(days=3)
    three_days_after_02272019 = three_days_after_02272019 + timedelta(days=3)
    days_passed_02012019_09302019 = date(2019, 9, 30) - date(2019, 1, 1)
    days_passed_02012019_09302019 = days_passed_02012019_09302019.days

    return (
        three_days_after_02272020,
        three_days_after_02272019,
        days_passed_02012019_09302019)


# PART 2

def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]:
    ''' returns a list of the line

        :param path: path to the file
        :type path: string

        :param fields: yhe number of fields exprected after splitting
        :type fields: int

        :param sep: seprator by ehich we have to split the string
        :type sep: string

        :param header: defaults to false, if true ignore the first line but after checking for appropriate fields
        :type header: bool

        :rtype: Iterator
        :return: Iterator[Tuple[str]]
    '''

    try:
        if len(path) == 0:
            raise ValueError('The path string cannot be empty')
        if not isinstance(path, str):
            raise ValueError('The path should be a string')
        if not isinstance(fields, int):
            raise ValueError('The fields should be an int')
        if not isinstance(sep, str):
            raise ValueError('The sep should be an string')
        if not isinstance(header, bool):
            raise ValueError('The header should be a bool')
    except ValueError as e:
        raise e

    try:
        file = open(path, 'r')
    except FileNotFoundError as e:
        raise e

    lines: List[str] = file.readlines()

    start = 0
    if header:
        start = 1

    for i in range(len(lines)):
        line = lines[i].rstrip()
        line_list = line.split(sep)
        if len(line_list) != fields:
            n: int = len(line_list)
            raise ValueError(
                f'{path} has {n} fields on line {i+1} expected {fields}')

        if start == 1:
            start = 0
            continue

        yield line_list


# PART 3

class FileAnalyzer:
    def __init__(self, directory):
        ''' Intializer functions just pass the directory path before calling this class

        :param None
        :type None

        :rtype: None
        :return: None
        '''

        self.directory = directory
        os.chdir(directory)
        self.listdir = os.listdir()
        self.files_summary: Dict[str, Dict[str, int]] = {}
        self.analyze_files()

    def analyze_files(self):
        ''' analyse the files and store ans in files summary

        :param None
        :type None

        :rtype: None
        :return: None
        '''

        py_files: list = []
        for file_name in self.listdir:
            if '.py' in file_name:
                py_files.append(file_name)

        for name in py_files:
            try:
                file = open(self.directory + '/' + name, 'r')
            except FileNotFoundError:
                print(
                    'Error!. The specified file was not found or it was unable to open')

            def_count: int = 0
            class_count: int = 0
            line_count: int = 0
            character_count: int = 0
            for line in file:
                if 'def ' in line:
                    def_count += 1

                if 'class ' in line:
                    class_count += 1

                line_count += 1
                character_count += len(line)

            self.files_summary[name] = {
                'class': class_count,
                'function': def_count,
                'line': line_count,
                'char': character_count}

    def pretty_print(self) -> None:
        ''' pretty print the data

        :param None
        :type None

        :rtype: None
        :return: None
        '''

        x = PrettyTable()
        x.field_names = ['File Name', 'Classes',
                         'Functions', 'Lines', 'Characters']
        for k, l in self.files_summary.items():
            row = [self.directory + '/' + k]
            row.extend(l.values())
            x.add_row(row)
        print("summary for ", self.directory)
        print(x)
