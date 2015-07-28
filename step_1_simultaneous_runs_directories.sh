#!/bin/bash
# This script creates the direcotry structure required for simultaneous 
# SPECFEM runs. The CMTSOLUTION for every event has to be copied to every 
# run directory manually

echo "Please enter the number of simultaneous runs (between 2 and 99): "                                               
read no_of_runs                                                                                                        

mkdir run0001
cd run0001
mkdir OUTPUT_FILES DATA SEM
cd DATA
ln -s ../../DATA/cemRequest/ .
cp ../../DATA/CMTSOLUTION .
cp ../../DATA/STATIONS .
cd ..
ln -s ../DATABASES_MPI .
cd OUTPUT_FILES
ln -s ../../OUTPUT_FILES/* .
                                                                                                                       
for i in `seq -f "%02g" 2 ${no_of_runs-1}`;                                                                            
    do                                                                                                                     
        cd ../..
        mkdir run00$i
        cd run00$i
        mkdir OUTPUT_FILES DATA SEM
        cd DATA
        ln -s ../../DATA/cemRequest/ .
        cp ../../DATA/CMTSOLUTION .
        cp ../../DATA/STATIONS .
        cd ..
        ln -s ../DATABASES_MPI .
        cd OUTPUT_FILES
        ln -s ../../OUTPUT_FILES/* .
    done                                                                                                                   

echo "Remember to move the individual CMTSOLUTION files to the respective"\
     " run directories or delete all other events from the large " \
     "CMTSOLUTION file that already is in every run00xx directory."
