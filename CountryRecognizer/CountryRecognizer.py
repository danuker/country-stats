"""
    This script translates the names of countries to country codes
"""
from logging import warning
import os
import re


class CountryRecognizer():
    def __init__(self, code_filename=None):
        if code_filename is None:
            code_filename = os.path.join(os.path.dirname(__file__), 'country_codes.csv')

        self.codes = {}     # Get code from country name
        self.countries = {} # Get country name from code (first occurrence)

        with open(code_filename) as f:
            for line in f:
                try:
                    _, country, comma, c2, _ = line.strip().split('"')

                    # Lowercase, remove irrelevant stuff,
                    c1 = self.normalize(country)
                    c2 = c2.strip('"')

                    self.codes[c1] = c2
                    if c2 not in self.countries:
                        self.countries[c2] = country

                except ValueError:
                    raise ValueError("ValueError at line: {}".format(line))
        #print("Loaded {} names for {} countries.".format(len(self.codes), len(self.countries)))

    @staticmethod
    def filter(name):
        """ Get rid of extra spaces and stop words """
        good_words = []
        list_of_words_maybe = name.split()
        for word in list_of_words_maybe:
            if word in ['and', 'of', 'the', 'former', 'state', 'plurinational', 'republic']:
                pass
            elif len(word) <= 1:
                pass
            else:
                good_words.append(word)
        return ' '.join(good_words)

    def normalize(self, natural_name):
        """
        Removes irrelevant words
        """
        nn = natural_name.lower().strip()\
            .replace("st.", "saint")

        paren = re.compile('\(.*?\)')          # Remove everything in parenthesis - but
                                               # match reluctantly - keep ( ) _this_ ( )
        nonalpha = re.compile('[^a-z ]')    # Remove everything not lowercase latin
        return self.filter(nonalpha.sub(' ', paren.sub(' ', nn)))

    def detect(self, natural_name):
        nn = self.normalize(natural_name)

        if nn in self.codes:
            return self.codes[nn]
        else:
            warning("Undetected country: '{}' (as '{}', added a '-' )".format(natural_name, nn))
            return '-'+natural_name

    def expand(self, code):
        if code in self.countries:
            return self.countries[code]
        else:
            warning("Undetected country code: '{}', added a '-' ".format(code))
            return '-'+code
