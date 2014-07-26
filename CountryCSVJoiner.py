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


def csvize(elems):
    return ','.join(map(lambda x: '"'+str(x)+'"', elems))

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return

    cr = CountryRecognizer()
    titles1, titles2 = ('',), ('',)
    table = {}

    with open(sys.argv[1], 'rb') as in1:
        r1 = csv.reader(in1)
        titles1 = r1.next()
        for stats in r1:
            code = cr.detect(stats[0])
            if code is None:
                continue
            table[code] = stats[1:] + (['']* (len(titles1[1:]) - len(stats[1:]) ))

    with open(sys.argv[2], 'rb') as in2:
        r2 = csv.reader(in2)
        titles2 = r2.next()
        for stats in r2:
            code = cr.detect(stats[0])
            if code is None:
                continue
            if code not in table:
                table[code] = ['']* (len(titles1)-1)
            table[code] += stats[1:]



    print(csvize(titles1 + titles2[1:]))
    for code in sorted(table.keys()):
        print(csvize([cr.expand(code)] + table[code]))


if __name__ == '__main__':
    main()
