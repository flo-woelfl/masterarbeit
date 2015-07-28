#!/bin/bash
# script to move the STATIONS_ADJOINT files to the correct position

echo "Please enter the number of simultaneous runs (between 2 and 99): "
read no_of_runs

for i in `seq -f "%02g" 1 ${no_of_runs-1}`;
do
    mv run00$i/SEM/STATIONS_ADJOINT run00$i/DATA/.
done
