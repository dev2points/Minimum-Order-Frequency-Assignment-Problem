TO=900
MO=8000
GLU_RESULTS_DIR=results/glucose4/nsc_assumptions 
CAD_RESULTS_DIR=results/cadical195/nsc_assumptions 
mkdir -p $CAD_RESULTS_DIR
mkdir -p $GLU_RESULTS_DIR

runlim -r $TO -s $MO  python3 -u main.py scen01 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u main.py scen02 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u main.py scen03 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u main.py scen04 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u main.py scen11 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen11.log
runlim -r $TO -s $MO  python3 -u main.py graph01 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u main.py graph02 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u main.py graph08 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u main.py graph14 nsc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph14.log

runlim -r $TO -s $MO  python3 -u main.py scen01 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u main.py scen02 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u main.py scen03 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u main.py scen04 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u main.py scen11 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen11.log
runlim -r $TO -s $MO  python3 -u main.py graph01 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u main.py graph02 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u main.py graph08 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u main.py graph14 nsc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph14.log