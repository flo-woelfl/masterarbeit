#/bin/bash
# DO NOT USE environment = COPY_ALL
#@ job_type = MPICH
#@ class = large
## node = 4
#@ total_tasks=12800
## other example
##@tasks_per_node = 39
#@ wall_clock_limit = 0:30:00
#@ job_name = smooth_50_event_kernels
#@ network.MPI = sn_all,not_shared,us
#@ initialdir = /gss/scratch/pr63qo/di29pod/specfem_all_50_runs 
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
#module load netcdf/mpi  # this caused problems so I commented it out, however this should normally be loaded 

mpiexec -np 12800 ./bin/xsmooth_sem 250 5 beta_kernel OUTPUT_SUM smooth_beta_misfit 
