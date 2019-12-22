# pulsar-pipeline

A small pipeline program for class. Given the search area, the pipeline will look for pulsars in that area from [ATNF pulsar catelogue](https://www.atnf.csiro.au/research/pulsar/psrcat/) and calculate the expected electron (or positron) spectra.

Reference article: [Fang K., Bi X.-J., Yin P.-F., Yuan Q., 2018, ApJ, 863, 30](https://doi.org/10.3847/1538-4357/aad092)

## Requirement

- python modules:
  - numpy
  - matplotlib
  - requests
  - beautifulsoup4
- gfortran
- latex compiler (pdflatex)

## Usage

The script `pulsar-pipeline` is a wrapping script around all other programs:

```sh
./pulsar-pipeline <ra> <dec> <radius> [-j <threads>]
```

It accepts three positional arguments: center coordinates `ra`, `dec` and search radius `radius` for pulsar sources, and an optional argument `-j` to specify number of threads for parallel calculation.

**Parallel execution:** Note that by default the pipeline will use all threads available.

The commands below are equivalent to what happens under the hood step by step:

```sh
gfortran FVM.f90 -o FVM
python ./fetchdata.py -c <ra> <dec> -r <radius>
python ./run.py ./FVM [-j <threads>]
python ./plot.py
```

## Output

all the generated files will be stored in a new `result` folder:

- **`report.pdf`**: generated report, final product
- **`rawdata.csv`**: fetched pulsar data
- **`data.csv`**: pulsar data formatted for easy use in calculation
- **`log/`**: program logging output
- **`output/`**: program generated data
- **`plots/`**: individual plots
- **`tex/`**: latex files for final report

## Credits

Bao Yiwei: the core fortran program to do the numerical calculation.

Lu Xu: python scripts to download data, start calculation and generate report pdf file.
