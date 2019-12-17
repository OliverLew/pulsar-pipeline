#!/usr/bin/env python
import os
import csv
import logging
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt  # noqa

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")


def ploteach(source):
    name = source['JName']
    plt.figure(figsize=(8, 6))
    plt.title('Source: {}'.format(name))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('$E$')
    plt.ylabel('$E^{3}flux$')
    for txt in os.listdir(outputdir):
        if txt.startswith(name):
            alpha = float(txt[len(name) + 1: -4])
            # filter data below floating point precision
            E, flux = np.loadtxt(os.path.join(outputdir, txt)).T
            E3flux = flux * E**3
            mask = (flux > 1e-308) * (E > 1e5)
            plt.plot(E[mask], E3flux[mask],
                     label='$\\alpha={}$'.format(alpha))
    plt.legend(framealpha=1)
    plt.savefig(os.path.join(plotdir, "{}.png".format(name)))
    plt.savefig(os.path.join(plotdir, "{}.eps".format(name)))
    plt.close()


if __name__ == '__main__':
    resultdir = "result"
    outputdir = os.path.join(resultdir, "output")
    plotdir = os.path.join(resultdir, "plots")
    if not os.path.exists(plotdir):
        os.mkdir(plotdir)

    with open("jobfile") as f:
        ra0, dec0, radius = [float(i) for i in f.read().split()]

    with open(os.path.join(resultdir, "data.csv")) as f:
        plt.figure()
        plt.title("Ra: ${}^\\circ$, Dec: ${}^\\circ$, radius: ${}^\\circ$"
                  .format(ra0, dec0, radius))
        plt.xlim((ra0 - radius, ra0 + radius))
        plt.ylim((dec0 - radius, dec0 + radius))
        plt.grid(lw=0.5, ls='--')
        for source in csv.DictReader(f):
            ra = float(source['RaJD'])
            dec = float(source['DecJD'])
            dist = float(source['Dist'])
            age = float(source['Age'])
            if dist > 2e3 or age < 1e4 * 365 * 24 * 60 * 60:
                filtered, = plt.plot(ra, dec, 'ro')
            else:
                accepted, = plt.plot(ra, dec, 'go')
                ploteach(source)
            plt.annotate(source['JName'], xy=(ra, dec),
                         xytext=(ra + radius / 50, dec + radius / 50))
        plt.legend([accepted, filtered], ['used', 'not used'], framealpha=1)
        plt.savefig(os.path.join(resultdir, "position.eps"))
