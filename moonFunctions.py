import re
from datetime import datetime

test = "Moon phase details at 3 May 2011"

def date_from_moon_string(s):
    sstr = str(s)
    print(sstr)
    return datetime.strptime(sstr, "%d %B %Y")

def make_ditance_float(d):
    print(d)

#date_from_moon_string(test)
