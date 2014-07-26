import os

__author__ = 'dan'

import unittest
from CountryRecognizer import CountryRecognizer


class MyTestCase(unittest.TestCase):
    def test_recognition(self):
        cr = CountryRecognizer()
        self.assertEqual('PL', cr.detect('Poland '))
        self.assertEqual('RO', cr.detect(' romania%#@  '))
        self.assertEqual('KP', cr.detect(' north korea'), )
        self.assertEqual('LA', cr.detect(" Lao People's Democratic Republic "))
        self.assertEqual('LA', cr.detect(" Laos "))

    def test_with_file(self):
        cr = CountryRecognizer()
        with open(os.path.join(os.path.dirname(__file__), 'country test.txt'), 'r') as f:
            for line in f:
                cr.detect(line)

    def test_with_code(self):
        cr = CountryRecognizer()
        with open(os.path.join(os.path.dirname(__file__), 'code_test.csv'), 'r') as f:
            for line in f:
                code = line[1:3]
                ctry = line.split('"')[3]
                self.assertEqual(code, cr.detect(ctry))

    def test_expansion(self):
        cr = CountryRecognizer()
        self.assertEqual("China", cr.expand("CN"))


if __name__ == '__main__':
    unittest.main()
