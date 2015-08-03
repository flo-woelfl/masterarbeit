#/bin/bash
# DO NOT USE environment = COPY_ALL
#@ job_type = MPICH
#@ class = test
## node = 4
#@ total_tasks=512
## other example
##@tasks_per_node = 39
#@ wall_clock_limit = 0:30:00
#@ job_name = CEM_2events_mesh
#@ network.MPI = sn_all,not_shared,us
#@ initialdir = /gpfs/work/pr63qo/di29pod/specfem_1st_round
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

mpiexec -np 512 ./bin/xmeshfem3D
