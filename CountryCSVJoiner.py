"""
    This script joins two CSVs of countries and stats.
    Usage:
        python CountryCSVJoiner.py in1.csv, in2.csv > out.csv

    Input format:
        Something   Stat1       Stat2   ....
        Afghanistan 0.01        0.3123
        Argentina   3.1         123.4
        ....
"""
import sys
import csv
from CountryRecognizer.CountryRecognizer import CountryRecognizer


def main():

    if len(sys.argv) != 3:
        print(__doc__)

    cr = CountryRecognizer()

    with open(sys.argv[1], 'rb') as in1:
        r1 = csv.reader(in1)
    with open(sys.argv[2], 'rb') as in2:
        r2 = csv.reader(in2)


if __name__ == '__main__':
    main()
