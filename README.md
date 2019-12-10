# pulsar-pipeline

WIP

current workflow:

```sh
python fetchdata.py -c <ra> <dec> -r <radius>
gfortran FVM.f90 -o FVM
python run.py FVM
```

Or use the wrapping script `go`, change the parameters within it.
