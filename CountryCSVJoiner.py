"""
This script joins two CSVs of countries and stats.
Usage:
    python CountryCSVJoiner.py in1.csv, in2.csv, ... > out.csv

Input format:
    Something   Stat1       Stat2   ....
    Afghanistan 0.01        0.3123
    Argentina   3.1         123.4
    ....
"""


import sys
import csv
import pandas
from CountryRecognizer.CountryRecognizer import CountryRecognizer

FINAL_COUNTRY_COLUMN = 'Detected Countries'

def main():
    cr = CountryRecognizer()

    if len(sys.argv) <= 2:
        print(__doc__)
        return

    a = pandas.io.parsers.read_csv(sys.argv[1], header=0)
    original_name = a.columns.values.tolist()[0]
    a.rename(columns={original_name: FINAL_COUNTRY_COLUMN}, inplace=True)

    # Transform to codes
    a.ix[:, 0] = a.ix[:, 0].apply(cr.detect)
    a = a.set_index(a.ix[:, 0])

    for arg in sys.argv[2:]:
        # Read the next csv in args
        a2 = pandas.io.parsers.read_csv(arg, header=0)

        # Set the (hopefully) detected country code of the first column as its index
        a2.ix[:, 0] = a2.ix[:, 0].apply(cr.detect)
        a2 = a2.set_index(a2.ix[:, 0])

        my_country_column = a2.columns[0]
        a = a.merge(a2,
                    left_on=FINAL_COUNTRY_COLUMN,
                    right_on=my_country_column,
                    how='outer')
        a.ix[:, 0] = a.ix[:, 0].combine_first(a.ix[:, my_country_column])
        a = a.drop(my_country_column, axis=1)

    a = pandas.DataFrame(a).sort(columns=[FINAL_COUNTRY_COLUMN])

    # Expand codes back to human names
    a.ix[:, 0] = a.ix[:, 0].apply(cr.expand)
    print(a.to_csv(quoting=True, index=False))


if __name__ == '__main__':
    main()
