./nsc_assumptions_no_preprocessing.sh
./tot_assumptions_no_preprocessing.sh
./remain.sh

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
