#!/bin/bash
mkdir run0001
cd run0001
mkdir OUTPUT_FILES DATA
cd DATA
ln -s ../../DATA/cemRequest/ .
cd ..
ln -s ../DATABASES_MPI .
cd OUTPUT_FILES
ln -s ../../OUTPUT_FILES/* .

cd ../..

mkdir run0010
cd run0010
mkdir OUTPUT_FILES DATA
ln -s ../DATABASES_MPI .
cd OUTPUT_FILES
ln -s ../../OUTPUT_FILES/* .

for i in `seq 2 9`;
do
    cd ../..
    mkdir run000$i 
    cd run000$i
    mkdir OUTPUT_FILES DATA
    cd DATA
    ln -s ../../DATA/cemRequest/ .
    cd ..
    ln -s ../DATABASES_MPI .
    cd OUTPUT_FILES
    ln -s ../../OUTPUT_FILES/* .
done
