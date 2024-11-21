"""
Helper functions for 'F1-ELO-Engine-2.0' repository
"""

import csv

from models import *

def read_csv_data(path):
    f = open(path)
    reader = csv.reader(f)

    # Skip the first line
    next(reader)

    return reader