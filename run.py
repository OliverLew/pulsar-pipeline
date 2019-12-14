#!/usr/bin/env python
import os
import sys
import csv
import logging
from subprocess import run, PIPE

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")


def runeach(source, alpha):
    data = "{} {} {} {}".format(source['Age'], source['Dist'],
                                source['Edot'], alpha)
    logging.info("Running source {}".format(source['JName']))
    logging.info(data)
    p = run([sys.argv[1]], stdout=PIPE,
            input=data, encoding='ascii')

    difelec_file = "{}-{}.txt".format(source['JName'], alpha)
    with open(os.path.join(outputdir, difelec_file), 'w') as f:
        f.write(p.stdout)
        f.flush()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.error("Pass the fortran executable as the argument")
        exit(1)
    if not os.path.exists("filterdata.csv"):
        logging.error("\"filterdata.csv\" does not exist, run fetchdata.py")
        exit(1)

    resultdir = "result"
    if not os.path.exists(resultdir):
        os.mkdir(resultdir)
    outputdir = os.path.join(resultdir, "output")
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    with open("filterdata.csv") as f:
        for source in csv.DictReader(f):
            for alpha in [1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]:
                runeach(source, alpha)
