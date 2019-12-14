#!/usr/bin/env python
import os
import sys
import csv
import logging
import argparse
from subprocess import run, PIPE
import multiprocessing as mp

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")


def runeach(source, alpha):
    data = "{} {} {} {}".format(source['Age'], source['Dist'],
                                source['Edot'], alpha)
    logging.info("Running source {}".format(source['JName']))
    logging.info(data)
    p = run([args.bin], stdout=PIPE,
            input=data, encoding='ascii')

    difelec_file = "{}-{}.txt".format(source['JName'], alpha)
    with open(os.path.join(outputdir, difelec_file), 'w') as f:
        f.write(p.stdout)
        f.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bin', help='the program to do the calculation')
    parser.add_argument('-j', '--threads', type=int)
    args = parser.parse_args()

    if not os.path.exists("filterdata.csv"):
        logging.error("\"filterdata.csv\" does not exist, run fetchdata.py")
        exit(1)

    resultdir = "result"
    outputdir = os.path.join(resultdir, "output")
    logdir = os.path.join(resultdir, "log")
    for d in [resultdir, outputdir, logdir]:
        if not os.path.exists(d):
            os.mkdir(d)

    if args.threads:
        num_threads = args.threads
    else:
        num_threads = mp.cpu_count()
    pool = mp.Pool(num_threads)

    with open("filterdata.csv") as f:
        for source in csv.DictReader(f):
            for alpha in [1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]:
                pool.apply_async(runeach, args=(source, alpha))
                # single thread
                #  runeach(source, alpha)
    pool.close()
    pool.join()
