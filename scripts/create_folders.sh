#!/bin/bash
mkdir run0001
cd run0001
mkdir OUTPUT_FILES DATA
ln -s ../DATABASES_MPI .
cd OUTPUT_FILES
ln -s ../../OUTPUT_FILES/* .

for i in 'seq 2 10';
do 
    cd ../../run000$i
    mkdir OUTPUT_FILES DATA
    ln -s ../DATABASES_MPI .
    cd OUTPUT_FILES
    ln -s ../../OUTPUT_FILES/* .
done
