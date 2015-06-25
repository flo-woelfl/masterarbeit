#!/bin/bash
# DO NOT USE environment = COPY_ALL
#@ job_type = MPICH
#@ class = test
## node = 4
#@ total_tasks=156
## other example
##@tasks_per_node = 39
#@ wall_clock_limit = 0:30:00
##                    1 h 20 min 30 secs
#@ job_name = specfem_test
#@ network.MPI = sn_all,not_shared,us
#@ initialdir = $(home)/specfem3d_globe/EXAMPLES/regional_MiddleEast
#@ output = job$(jobid).out
#@ error = job$(jobid).err
#@ notification=always
#@ notify_user=fwoelfl@geophysik.uni-muenchen.de
#@ queue
. /etc/profile
. /etc/profile.d/modules.sh
#setup of environment
module unload mpi.ibm
module unload paraview
module load mpi.intel
module load hdf5/mpi
module load netcdf/mpi

# echo `date`
# echo "starting MPI mesher on $numnodes processors"                                                                   
# echo                                                                                                                 
#  
# mpiexec -np $numnodes $PWD/bin/xmeshfem3D                                                                            
#  
# echo "  mesher done: `date`"                                                                                         
# echo                                                                                                                 
# 
# # backup important files addressing.txt and list*.txt                                                                
# cp OUTPUT_FILES/*.txt $BASEMPIDIR/                                                                                   
#                                                                                                                       
#  
# ##
# ## forward simulation                                                                                                
# ##                                                                                                                   
#  
# # set up addressing
# cp $BASEMPIDIR/addr*.txt OUTPUT_FILES/                                                                              
# cp $BASEMPIDIR/list*.txt OUTPUT_FILES/                                                                              
#                                                                                                               
# echo
# echo `date`
# echo starting run in current directory $PWD
# echo

mpiexec -np 64 ./bin/xspecfem3D
 
echo "finished successfully"
# echo `date`

