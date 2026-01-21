TO=900
MO=8000
GLU_RESULTS_DIR=results/glucose4/nsc_incremental 
CAD_RESULTS_DIR=results/cadical195/nsc_incremental 
mkdir -p $CAD_RESULTS_DIR
mkdir -p $GLU_RESULTS_DIR

# runlim -r $TO -s $MO  python3 -u main.py scen01 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen01.log
# runlim -r $TO -s $MO  python3 -u main.py scen02 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen02.log
# runlim -r $TO -s $MO  python3 -u main.py scen03 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen03.log
# runlim -r $TO -s $MO  python3 -u main.py scen04 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen04.log
# runlim -r $TO -s $MO  python3 -u main.py scen11 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/scen11.log
# runlim -r $TO -s $MO  python3 -u main.py graph01 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph01.log
# runlim -r $TO -s $MO  python3 -u main.py graph02 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph02.log
# runlim -r $TO -s $MO  python3 -u main.py graph08 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph08.log
# runlim -r $TO -s $MO  python3 -u main.py graph09 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph09.log
# runlim -r $TO -s $MO  python3 -u main.py graph14 nsc incremental glucose4 2>&1 | tee $GLU_RESULTS_DIR/graph14.log

runlim -r $TO -s $MO  python3 -u main.py scen01 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u main.py scen02 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u main.py scen03 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u main.py scen04 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u main.py scen11 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen11.log
runlim -r $TO -s $MO  python3 -u main.py graph01 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u main.py graph02 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u main.py graph08 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u main.py graph14 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph14.log

runlim -r $TO -s $MO  python3 -u main.py graph03 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph03.log
runlim -r $TO -s $MO  python3 -u main.py graph04 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph04.log
runlim -r $TO -s $MO  python3 -u main.py graph05 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph05.log
runlim -r $TO -s $MO  python3 -u main.py graph06 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph06.log
runlim -r $TO -s $MO  python3 -u main.py graph07 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph07.log
runlim -r $TO -s $MO  python3 -u main.py graph10 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph10.log
runlim -r $TO -s $MO  python3 -u main.py graph11 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph11.log
runlim -r $TO -s $MO  python3 -u main.py graph12 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph12.log
runlim -r $TO -s $MO  python3 -u main.py graph13 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph13.log
runlim -r $TO -s $MO  python3 -u main.py scen05 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen05.log
runlim -r $TO -s $MO  python3 -u main.py scen06 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen06.log
runlim -r $TO -s $MO  python3 -u main.py scen07 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen07.log
runlim -r $TO -s $MO  python3 -u main.py scen08 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen08.log
runlim -r $TO -s $MO  python3 -u main.py scen09 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen09.log
runlim -r $TO -s $MO  python3 -u main.py scen10 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen10.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.1 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.1.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.2 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.2.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.3 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.3.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.4 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.4.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.5 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.5.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.1 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.1.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.2 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.2.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.3 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.3.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.4 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.4.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.5 nsc incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.5.log