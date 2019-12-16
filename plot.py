#!/usr/bin/env python
import os
import csv
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt  # noqa


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
            plt.plot(E[flux > 1e-308], E3flux[flux > 1e-308],
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

    with open("filterdata.csv") as f:
        for source in csv.DictReader(f):
            ploteach(source)
