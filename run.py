#!/usr/bin/env python
import os
import csv
import logging
import argparse
from subprocess import run, PIPE
import multiprocessing as mp

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")


def runeach(source, alpha):
    data = "{} {} {} {} {}".format(source['JName'], source['Age'],
                                   source['Dist'], source['Edot'], alpha)
    logging.info("Running source {}, alpha={}".format(source['JName'], alpha))
    logging.info("input: {}".format(data))

    p = run([args.bin], stdout=PIPE, input=data, encoding='ascii')

    difelec_file = "{}-{}.txt".format(source['JName'], alpha)
    with open(os.path.join(outputdir, difelec_file), 'w') as f:
        f.write(p.stdout)
        f.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bin', help='the program to do the calculation')
    parser.add_argument('-j', '--threads', type=int)
    args = parser.parse_args()

    resultdir = "result"
    currentdir = os.path.dirname(__file__)
    resultdir = os.path.join(currentdir, "result")
    outputdir = os.path.join(resultdir, "output")
    logdir = os.path.join(resultdir, "log")
    for d in [resultdir, outputdir, logdir]:
        if not os.path.exists(d):
            os.mkdir(d)

    data_file = os.path.join(resultdir, "data.csv")
    if not os.path.exists(data_file):
        logging.error("\"data.csv\" does not exist, run fetchdata.py")
        exit(1)

    if args.threads:
        num_threads = args.threads
    else:
        num_threads = mp.cpu_count()
    pool = mp.Pool(num_threads)

    with open(data_file) as f:
        for source in csv.DictReader(f):
            if source['Dist'] == "*" or source['Age'] == "*" \
                    or source['Edot'] == "*":
                continue
            if float(source['Dist']) > 2e3:
                continue
            if float(source['Age']) < 1e4 * 365.25 * 24 * 60 * 60:
                continue
            for alpha in [1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]:
                pool.apply_async(runeach, args=(source, alpha))

    pool.close()
    pool.join()
