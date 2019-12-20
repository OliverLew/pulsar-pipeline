#!/usr/bin/env python
import os
import csv
import logging
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt  # noqa
from subprocess import run, PIPE  # noqa

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")


def ploteach(source):
    name = source['JName']
    plt.figure(figsize=(5, 4))
    plt.title('Source: ${}$'.format(name))
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
    plt.tight_layout()
    plt.savefig(os.path.join(plotdir, "{}.eps".format(name)))
    plt.close()


class Pdf():
    def __init__(self):
        self.texfile = os.path.join(texdir, "report.tex")
        self.preamble = ("\\documentclass{article}\n" +
                         "\\nonstopmode\n" +
                         "\\usepackage{graphicx}\n")
        self.map = ("\\begin{figure}\n" +
                    "\\includegraphics[width=\\textwidth]{" +
                    os.path.join(plotdir, "position") +
                    "}\n" +
                    "\\end{figure}\n")
        self.figures = []
        self.tablerows = []

        self.tableheader = " & ".join(["Source Name",
                                       "Age",
                                       "Distance",
                                       "$\\dot{E}$",
                                       "Ra",
                                       "Dec"]) + '\\\\\n' + \
                           " & ".join(["",
                                       "(yr)",
                                       "(kpc)",
                                       "$(m_ec^2/s)$",
                                       "(degree)",
                                       "(degree)"])

    def addtablerow(self, data):
        self.tablerows.append(" & ".join(list(data)))

    def addfigure(self, sourcename):
        self.figures.append("\\begin{figure}\n" +
                            "\\includegraphics[width=0.8\\textwidth]{" +
                            os.path.join(plotdir, sourcename) +
                            "}\n" +
                            "\\end{figure}\n")

    def compile(self):
        with open(self.texfile, 'w') as f:
            f.write(self.preamble)
            f.write("\\begin{document}\n")
            f.write(self.map)
            f.write("\\begin{center}\n\\begin{tabular}{*{6}{c}}\n")
            f.write(self.tableheader + "\\\\\n")
            f.write("\\hline\n")
            f.write("\\\\\n".join(self.tablerows) + "\\\\\n")
            f.write("\\end{tabular}\n\\end{center}\n")
            f.write("".join(self.figures))
            f.write("\\end{document}\n")
        p = run(["pdflatex", "-output-directory", texdir, self.texfile],
                stdout=PIPE, stderr=PIPE)
        if p.returncode:
            logging.error(p.stdout.decode("utf-8"))
            logging.error(p.stderr.decode("utf-8"))
            logging.error("pdf compile failed")
        else:
            os.rename(os.path.join(texdir, "report.pdf"),
                      os.path.join(resultdir, "report.pdf"))


if __name__ == '__main__':
    currentdir = os.path.dirname(__file__)
    resultdir = os.path.join(currentdir, "result")
    outputdir = os.path.join(resultdir, "output")
    plotdir = os.path.join(resultdir, "plots")
    texdir = os.path.join(resultdir, "tex")
    for d in [plotdir, texdir]:
        if not os.path.exists(d):
            os.mkdir(d)

    with open(os.path.join(currentdir, "jobfile")) as f:
        ra0, dec0, radius = [float(i) for i in f.read().split()]

    with open(os.path.join(resultdir, "data.csv")) as f:
        pdf = Pdf()
        plt.figure()
        plt.title("Ra: ${}^\\circ$, Dec: ${}^\\circ$, radius: ${}^\\circ$"
                  .format(ra0, dec0, radius))
        plt.xlim((ra0 - radius, ra0 + radius))
        plt.ylim((dec0 - radius, dec0 + radius))
        plt.grid(lw=0.5, ls='--')

        for source in csv.DictReader(f):
            ra = float(source['RaJD'])
            dec = float(source['DecJD'])
            dist = float(source['Dist']) / 1e3
            age = float(source['Age']) / (365.25 * 24 * 60 * 60)
            edot = float(source['Edot'])
            if dist > 2 or age < 1e4:
                filtered, = plt.plot(ra, dec, 'ro')
            else:
                accepted, = plt.plot(ra, dec, 'go')
                ploteach(source)
                pdf.addfigure(source['JName'])
            plt.annotate(source['JName'], xy=(ra, dec),
                         xytext=(ra + radius / 50, dec + radius / 50))
            pdf.addtablerow([source['JName'],
                             "{:.1e}".format(age),
                             "{:.2f}".format(dist),
                             "{:.2e}".format(edot),
                             "{:.2f}".format(ra),
                             "{:.2f}".format(dec)])
        plt.legend([accepted, filtered], ['used', 'not used'], framealpha=1)
        plt.savefig(os.path.join(plotdir, "position.eps"))
        pdf.compile()
