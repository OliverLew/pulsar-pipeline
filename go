#!/usr/bin/env python
import os
import logging
import argparse
import subprocess

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")

pkgs = []
for pkg in [{"module": "bs4", "package": "beautifulsoup4"},
            {"module": "requests", "package": "requests"},
            {"module": "numpy", "package": "numpy"},
            {"module": "matplotlib", "package": "matplotlib"}]:
    try:
        __import__(pkg["module"])
    except ImportError:
        pkgs.append(pkg["package"])
if len(pkgs) > 0:
    logging.info("please install the following python modules:")
    logging.info("\t{}".format("\n\t".join(pkgs)))
    logging.info("pip install --user {}".format(" ".join(pkgs)))
    exit(1)

parser = argparse.ArgumentParser(description="")
parser.add_argument('ra', nargs="?", default="97", help="unit: degree")
parser.add_argument('dec', nargs="?", default="8", help="unit: degree")
parser.add_argument('radius', nargs="?", default="2", help="unit: degree")
parser.add_argument('-j', '--threads', help="default to maximum available")
args = parser.parse_args()

if not os.path.exists("filterdata.csv"):
    p = subprocess.run(["python", "./fetchdata.py",
                        "-c", args.ra, args.dec,
                        "-r", args.radius])
    if p.returncode:
        exit(p.returncode)
else:
    logging.info("filterdata.csv exists! Using the current data file ...")

if subprocess.run(["gfortran", "./FVM.g90"]).returncode:
    exit(1)

if args.threads:
    p = subprocess.run(["python", "./run.py", "./FVM", "-j", args.threads])
else:
    p = subprocess.run(["python", "./run.py", "./FVM"])

if p.returncode:
    exit(p.returncode)

subprocess.run(["python", "./plot.py"])
