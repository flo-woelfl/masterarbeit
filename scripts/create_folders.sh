mkdir run0001 run0002
cd run0001
mkdir OUTPUT_FILES DATA
ln -s ../DATABASES_MPI .
cd OUTPUT_FILES
ln -s ../../OUTPUT_FILES/* .
cd ../../run0002
mkdir OUTPUT_FILES DATA
ln -s ../DATABASES_MPI .
cd OUTPUT_FILES
ln -s ../../OUTPUT_FILES/* .