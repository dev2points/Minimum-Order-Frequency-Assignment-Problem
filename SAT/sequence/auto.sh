# ./nsc_incremental.sh
# ./remain.sh
# ./nsc_assumptions.sh
# ./tot_assumptions.sh
./remain_symmetry.sh
./
cd ..
cd pairwise
./auto.sh
cd ..
cd Gurobi
./auto.sh
cd ..
cd CPLEX/CP
./auto.sh
cd ..
cd MIP
./auto.sh