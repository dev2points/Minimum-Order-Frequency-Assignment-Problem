TO=900
MO=8000
GLU_RESULTS_DIR=results/glucose4/sc_assumptions 
CAD_RESULTS_DIR=results/cadical195/sc_assumptions 
mkdir -p $CAD_RESULTS_DIR
mkdir -p $GLU_RESULTS_DIR

# runlim -r $TO -s $MO  python3 -u main.py scen01 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen01.log
# runlim -r $TO -s $MO  python3 -u main.py scen02 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen02.log
# runlim -r $TO -s $MO  python3 -u main.py scen03 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen03.log
# runlim -r $TO -s $MO  python3 -u main.py scen04 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen04.log
# runlim -r $TO -s $MO  python3 -u main.py scen11 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen11.log
# runlim -r $TO -s $MO  python3 -u main.py graph01 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph01.log
# runlim -r $TO -s $MO  python3 -u main.py graph02 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph02.log
# runlim -r $TO -s $MO  python3 -u main.py graph08 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph08.log
# runlim -r $TO -s $MO  python3 -u main.py graph09 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph09.log
# runlim -r $TO -s $MO  python3 -u main.py graph14 sc assumptions glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph14.log

# runlim -r $TO -s $MO  python3 -u main.py scen01 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen01.log
# runlim -r $TO -s $MO  python3 -u main.py scen02 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen02.log
# runlim -r $TO -s $MO  python3 -u main.py scen03 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen03.log
# runlim -r $TO -s $MO  python3 -u main.py scen04 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen04.log
# runlim -r $TO -s $MO  python3 -u main.py scen11 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen11.log
# runlim -r $TO -s $MO  python3 -u main.py graph01 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph01.log
# runlim -r $TO -s $MO  python3 -u main.py graph02 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph02.log
# runlim -r $TO -s $MO  python3 -u main.py graph08 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph08.log
# runlim -r $TO -s $MO  python3 -u main.py graph09 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph09.log
# runlim -r $TO -s $MO  python3 -u main.py graph14 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph14.log

runlim -r $TO -s $MO  python3 -u main.py graph03 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph03.log
runlim -r $TO -s $MO  python3 -u main.py graph04 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph04.log
runlim -r $TO -s $MO  python3 -u main.py graph05 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph05.log
runlim -r $TO -s $MO  python3 -u main.py graph06 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph06.log
runlim -r $TO -s $MO  python3 -u main.py graph07 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph07.log
runlim -r $TO -s $MO  python3 -u main.py graph10 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph10.log
runlim -r $TO -s $MO  python3 -u main.py graph11 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph11.log
runlim -r $TO -s $MO  python3 -u main.py graph12 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph12.log
runlim -r $TO -s $MO  python3 -u main.py graph13 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph13.log
runlim -r $TO -s $MO  python3 -u main.py scen05 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen05.log
runlim -r $TO -s $MO  python3 -u main.py scen06 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen06.log
runlim -r $TO -s $MO  python3 -u main.py scen07 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen08.log
runlim -r $TO -s $MO  python3 -u main.py scen08 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen08.log
runlim -r $TO -s $MO  python3 -u main.py scen09 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen09.log
runlim -r $TO -s $MO  python3 -u main.py scen10 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen10.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.1 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.1.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.2 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.2.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.3 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.3.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.4 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.4.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.5 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.5.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.1 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.1.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.2 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.2.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.3 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.3.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.4 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.4.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.5 sc assumptions cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.5.log