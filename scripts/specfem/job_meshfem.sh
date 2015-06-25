#!/bin/bash
# DO NOT USE environment = COPY_ALL
#@ job_type = MPICH
#@ class = test
## node = 4
#@ total_tasks=64
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
module load mpi.intel
module load netcdf/mpi

# echo `date`
# echo "starting MPI mesher on $numnodes processors"                                                                   
# echo                                                                                                                 

mpiexec -np 64 ./bin/xmeshfem3D
 
# echo "  mesher done: `date`"                                                                                         
# echo                                                                                                                 

