import glob
import os
import unittest

import fileio as fio
import error

BASE_DIR = os.path.dirname(__name__)
TEST_DATA_DIR = os.path.join(BASE_DIR, 'test_data')

class FileReaderTestCase(unittest.TestCase):
    
    def test_get_csv_reader_success1(self):
        paths = glob.glob(os.path.join(TEST_DATA_DIR, 'success1.csv'))
        for path in paths:
            row_found = False
            for row in fio.get_csv_reader(path):
                row_found = True
                pass
            self.assertTrue(row_found)

    def test_get_csv_reader_success_header_but_no_data(self):
        paths = glob.glob(os.path.join(
            TEST_DATA_DIR, 'success_header_but_no_data.csv'))
        for path in paths:
            row_found = False
            for rowi, row in enumerate(fio.get_csv_reader(path)):
                row_found = True
            self.assertFalse(row_found)

    def test_get_csv_reader_error_missing_header(self):
        paths = glob.glob(
            os.path.join(TEST_DATA_DIR, 'error_missing_header.csv'))
        with self.assertRaises(error.MissingHeaderException):
            for path in paths:
                for row in fio.get_csv_reader(path):
                    pass

    def test_get_csv_reader_error_missing_latitude(self):
        paths = glob.glob(
            os.path.join(TEST_DATA_DIR, 'error_missing_latitude.csv'))
        with self.assertRaises(error.WrongHeaderException) as assert_obj:
            for path in paths:
                for row in fio.get_csv_reader(path):
                    pass
        self.assertEqual(assert_obj.exception.col_missing, 'Latitude')

    def test_get_csv_reader_error_missing_longitude(self):
        paths = glob.glob(
            os.path.join(TEST_DATA_DIR, 'error_missing_longitude.csv'))
        with self.assertRaises(error.WrongHeaderException) as assert_obj:
            for path in paths:
                for row in fio.get_csv_reader(path):
                    pass
        self.assertEqual(assert_obj.exception.col_missing, 'Longitude')

    def test_get_csv_reader_error_latitude_not_a_number(self):
        paths = glob.glob(
            os.path.join(TEST_DATA_DIR, 'error_latitude_not_a_number.csv'))
        with self.assertRaises(error.CoordinateNotANumber) as assert_obj:
            for path in paths:
                for row in fio.get_csv_reader(path):
                    pass
        self.assertEqual(assert_obj.exception.line_number, 1)
        self.assertEqual(assert_obj.exception.col, 'Latitude')
        self.assertEqual(assert_obj.exception.value, 'a39.90164701')

    def test_get_csv_reader_error_longitude_not_a_number(self):
        paths = glob.glob(
            os.path.join(TEST_DATA_DIR, 'error_longitude_not_a_number.csv'))
        with self.assertRaises(error.CoordinateNotANumber) as assert_obj:
            for path in paths:
                for row in fio.get_csv_reader(path):
                    pass
        self.assertEqual(assert_obj.exception.line_number, 1)
        self.assertEqual(assert_obj.exception.col, 'Longitude')
        self.assertEqual(assert_obj.exception.value, '-a95.60179108')
