#!/usr/bin/env python

import os
import csv
import logging
from subprocess import run, PIPE

logging.basicConfig(level=logging.INFO, format="%(message)s")


if __name__ == '__main__':
    with open("filterdata.csv") as f:
        count = 0
        reader = csv.DictReader(f)
        for data in reader:
            count = count + 1
            input = "{} {} {} {}".format(data['JName'], data['Age'],
                                           data['Dist'], data['Edot'])
            p = run(['cat'], stdout=PIPE, input=input, encoding='ascii')
            logging.info("Running source {}".format(count))
            print(p.stdout)
            print()
