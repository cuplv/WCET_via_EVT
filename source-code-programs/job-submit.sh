#!/bin/bash

#SBATCH --time=01:00:00
#SBATCH --output=job-output-seq_search-%j.out
#SBATCH --job-name=seq_search

module load python/2.7.14
module load jdk/1.8.0
export PYTHONPATH="$PYTHONPATH:/projects/$USER/python_libs/lib/python2.7/site-packages/"
export GUROBI_HOME="/home/sati3279/my_codes/gurobi810/linux64"
export PATH="${PATH}:${GUROBI_HOME}/bin"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"

echo "== Start of Job =="
date
python Random.py
date
echo "== End of Job =="
