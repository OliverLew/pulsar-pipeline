# pulsar-pipeline

## Requirement

- python modules:
  - numpy
  - matplotlib
  - requests
  - beautifulsoup4
- gfortran

## Output

all the generated files will be stored in a new `result` folder:

- **`report.pdf`**: generated report, final product
- **`rawdata.csv`**: fetched pulsar data
- **`data.csv`**: pulsar data formatted for easy use in calculation
- **`log/`**: program logging output
- **`output/`**: program generated data
- **`plots/`**: individual plots
- **`tex/`**: latex files

## Usage

The script `pulsar-pipeline` is a wrap scrip around all other programs:

```sh
./pulsar-pipeline <ra> <dec> <radius> [-j <threads>]
```

It accepts three positional arguments: center coordinates `ra`, `dec` and search radius `radius` for pulsar sources, and an optional argument `-j` to specify number of threads for parallel calculation.

**Note** that by default the pipeline will use all threads available.

The commands below is equivalent to what happens under the hood step by step:

```sh
gfortran FVM.f90 -o FVM
python ./fetchdata.py -c <ra> <dec> -r <radius>
python ./run.py ./FVM [-j <threads>]
python ./plot.py
```
