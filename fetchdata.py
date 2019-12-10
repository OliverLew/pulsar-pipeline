#!/usr/bin/env python
# NOTE: The whole database could also be downloaded from website:
# https://www.atnf.csiro.au/research/pulsar/psrcat/download.html

import os
import csv
import logging
import argparse
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(message)s")


def request_data(coor1, coor2, r):
    baseurl = "https://www.atnf.csiro.au/research/pulsar/psrcat/proc_form.php"
    parameters = {
        "version": "1.62",
        "JName": "JName",
        "Dist": "Dist",
        "Age": "Age",
        "Edot": "Edot",
        "startUserDefined": "true",
        "sort_attr": "jname",
        "sort_order": "asc",
        "condition": "",
        "ephemeris": "short",
        "coords_unit": "raj/decj",
        "radius": r,
        "coords_1": coor1,
        "coords_2": coor2,
        "style": "Short csv without errors",
        "no_value": "*",
        "fsize": "3",
        "x_axis": "",
        "x_scale": "linear",
        "y_axis": "",
        "y_scale": "linear",
        "state": "query",
        "table_bottom.x": "29",
        "table_bottom.y": "21"
    }

    try:
        res = requests.get(baseurl, params=parameters)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
        logging.error("Connection error, please re-run the script")
        exit(1)

    if res:
        soup = BeautifulSoup(res.content, 'html.parser')
        rawdata = soup.find("pre").string.strip() + '\n'
    else:
        logging.error("Download failed, please re-run the script")
        exit(1)

    with open("rawdata.csv", "w") as f:
        f.write(rawdata)

    with open("rawdata.csv") as rawdata, open("filterdata.csv", "w") as f:
        rawcount = 0
        filtercount = 0
        fields = ['JName', 'Age', 'Dist', 'Edot']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        reader = csv.DictReader(rawdata, delimiter=';')
        for data in reader:
            rawcount = rawcount + 1
            if data['#'] and data['DIST'] != '*' and data['AGE'] != '*' \
                    and data['EDOT'] != '*':
                if float(data['DIST']) > 2 or float(data['AGE']) < 1e4:
                    continue
                filtercount = filtercount + 1
                # convert unit from erg/s to m_e c^2/s
                Edot = float(data['EDOT']) * 1221432.8760283517
                # convert unit from kpc to pc
                Dist = float(data['DIST']) * 1e3
                # convert unit from yr to s
                Age = float(data['AGE']) * 365.25 * 24 * 60 * 60

                writer.writerow({'JName': data['PSRJ'],
                                 'Age': Age, 'Dist': Dist, 'Edot': Edot})
        logging.info("Data saved!")
        logging.info("Total: %d, filtered: %d" % (rawcount, filtercount))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--coor', nargs=2, metavar=("RaJ", "DecJ"))
    parser.add_argument('-r', '--radius', nargs=1, metavar="Radius")
    args = parser.parse_args()

    request_data(args.coor[0], args.coor[1], args.radius)
