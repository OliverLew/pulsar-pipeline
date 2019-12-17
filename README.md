# pulsar-pipeline

WIP

current workflow:

```sh
gfortran FVM.f90 -o FVM
python ./fetchdata.py -c <ra> <dec> -r <radius>
python ./run.py ./FVM [-j <threads>]
python ./plot.py
```

Or use the wrapping script `go`:

```sh
./go <ra> <dec> <radius> [-j <threads>]
```
