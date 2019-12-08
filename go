#!/bin/sh

if [ ! -f "filterdata.csv" ]; then
    python ./fetchdata.py -c 10 10 -r 10
else
    echo "filterdata.csv" already exists! Using the current data file ...
    echo
fi
python ./run.py
