"""
Helper functions for 'F1-Ratings_Engine' repository
"""

import csv

from models import *

def read_csv_data(path):
    f = open(path)
    reader = csv.reader(f)

    # Skip the first line
    next(reader)

    return reader