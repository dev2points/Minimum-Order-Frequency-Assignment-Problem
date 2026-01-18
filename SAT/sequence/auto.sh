# ./sc_assumptions.sh
# ./sc_incremental.sh
# ./nsc_assumptions.sh
# ./nsc_incremental.sh
# # ./tot_assumptions.sh
# # ./tot_incremental.sh
# ./sc_full_assumptions.sh
# ./sc_full_incremental.sh
# ./nsc_full_assumptions.sh
# ./nsc_full_incremental.sh
# # ./glucose4.sh
# # ./cadical195.sh

TO=900
MO=8000

runlim -r $TO -s $MO  python3 -u main.py scen07 sc incremental cadical195 2>&1 | tee results/cadical195/sc_incremental/scen07.log
runlim -r $TO -s $MO  python3 -u main.py scen07 sc assumptions cadical195 2>&1 | tee results/cadical195/sc_assumptions/scen07.log
runlim -r $TO -s $MO  python3 -u main.py scen07 sc_full incremental cadical195 2>&1 | tee results/cadical195/sc_full_incremental/scen07.log
runlim -r $TO -s $MO  python3 -u main.py scen07 sc_full assumptions cadical195 2>&1 | tee results/cadical195/sc_full_assumptions/scen07.log
runlim -r $TO -s $MO  python3 -u main.py scen07 nsc_full incremental cadical195 2>&1 | tee results/cadical195/nsc_full_incremental/scen07.log
runlim -r $TO -s $MO  python3 -u main.py scen07 nsc_full assumptions cadical195 2>&1 | tee results/cadical195/nsc_full_assumptions/scen07.log