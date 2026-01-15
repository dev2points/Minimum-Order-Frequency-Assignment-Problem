TO=900
MO=8000
GLU_RESULTS_DIR=results/glucose4/sc_incremental 
CAD_RESULTS_DIR=results/cadical195/sc_incremental 
mkdir -p $CAD_RESULTS_DIR
mkdir -p $GLU_RESULTS_DIR

runlim -r $TO -s $MO  python3 -u main.py scen01 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u main.py scen02 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u main.py scen03 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u main.py scen04 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u main.py scen11 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen11.log
runlim -r $TO -s $MO  python3 -u main.py graph01 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u main.py graph02 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u main.py graph08 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u main.py graph09 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u main.py graph14 sc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph14.log

runlim -r $TO -s $MO  python3 -u main.py scen01 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u main.py scen02 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u main.py scen03 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u main.py scen04 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u main.py scen11 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen11.log
runlim -r $TO -s $MO  python3 -u main.py graph01 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u main.py graph02 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u main.py graph08 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u main.py graph09 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u main.py graph14 sc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph14.log