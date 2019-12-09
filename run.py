#!/usr/bin/env python

import os
import sys
import csv
import logging
from subprocess import run

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.error("Pass the fortran executable as the argument")
        exit(1)
    if not os.path.exists("filterdata.csv"):
        logging.error("\"filterdata.csv\" does not exist, run fetchdata.py")
        exit(1)
    with open("filterdata.csv") as f:
        count = 0
        reader = csv.DictReader(f)
        for data in reader:
            count = count + 1
            inputdata = "{} {} {} {}".format(data['JName'], data['Age'],
                                             data['Dist'], data['Edot'])
            logging.info("Running source {}".format(count))
            logging.info(inputdata)
            p = run([sys.argv[1]], input=inputdata, encoding='ascii')
            print()
