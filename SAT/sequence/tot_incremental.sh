TO=900
MO=8000
GLU_RESULTS_DIR=results/glucose4/tot_incremental 
CAD_RESULTS_DIR=results/cadical195/tot_incremental 
mkdir -p $CAD_RESULTS_DIR
mkdir -p $GLU_RESULTS_DIR

# runlim -r $TO -s $MO  python3 -u main.py scen01 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen01.log
# runlim -r $TO -s $MO  python3 -u main.py scen02 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen02.log
# runlim -r $TO -s $MO  python3 -u main.py scen03 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen03.log
# runlim -r $TO -s $MO  python3 -u main.py scen04 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen04.log
# runlim -r $TO -s $MO  python3 -u main.py scen05 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen05.log
# runlim -r $TO -s $MO  python3 -u main.py scen11 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen11.log
# runlim -r $TO -s $MO  python3 -u main.py graph01 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph01.log
# runlim -r $TO -s $MO  python3 -u main.py graph02 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph02.log
# runlim -r $TO -s $MO  python3 -u main.py graph03 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph03.log
# runlim -r $TO -s $MO  python3 -u main.py graph04 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph04.log
# runlim -r $TO -s $MO  python3 -u main.py graph08 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph08.log
# runlim -r $TO -s $MO  python3 -u main.py graph09 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph09.log
# runlim -r $TO -s $MO  python3 -u main.py graph10 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph10.log
# runlim -r $TO -s $MO  python3 -u main.py graph14 tot incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph14.log

runlim -r $TO -s $MO  python3 -u main.py scen01 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u main.py scen02 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u main.py scen03 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u main.py scen04 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u main.py scen05 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen05.log
runlim -r $TO -s $MO  python3 -u main.py scen11 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen11.log
runlim -r $TO -s $MO  python3 -u main.py graph01 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u main.py graph02 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u main.py graph03 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph03.log
runlim -r $TO -s $MO  python3 -u main.py graph04 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph04.log
runlim -r $TO -s $MO  python3 -u main.py graph08 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u main.py graph09 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u main.py graph10 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph10.log
runlim -r $TO -s $MO  python3 -u main.py graph14 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph14.log