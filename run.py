#!/usr/bin/env python

import os
import sys
import csv
import logging
from subprocess import run, PIPE

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.error("Pass the fortran executable as the argument")
        exit(1)
    if not os.path.exists("filterdata.csv"):
        logging.error("\"filterdata.csv\" does not exist, run fetchdata.py first")
        exit(1)
    with open("filterdata.csv") as f:
        count = 0
        reader = csv.DictReader(f)
        for data in reader:
            count = count + 1
            input = "{} {} {} {}".format(data['JName'], data['Age'],
                                           data['Dist'], data['Edot'])
            p = run([sys.argv[1]], stdout=PIPE, input=input, encoding='ascii')
            logging.info("Running source {}".format(count))
            print(p.stdout)
            print()
