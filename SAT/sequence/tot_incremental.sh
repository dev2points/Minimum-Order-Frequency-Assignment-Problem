TO=600
MO=14000
GLU_RESULTS_DIR=results/glucose4/nsc_incremental 
CAD_RESULTS_DIR=results/cadical195/tot_incremental 
mkdir -p $CAD_RESULTS_DIR


runlim -r $TO -s $MO  python3 -u main.py scen01 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u main.py scen02 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u main.py scen03 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u main.py scen04 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u main.py scen11 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen11.log
runlim -r $TO -s $MO  python3 -u main.py graph01 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u main.py graph02 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u main.py graph08 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u main.py graph09 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u main.py graph14 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph14.log

runlim -r $TO -s $MO  python3 -u main.py graph03 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph03.log
runlim -r $TO -s $MO  python3 -u main.py graph04 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph04.log
runlim -r $TO -s $MO  python3 -u main.py graph05 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph05.log
runlim -r $TO -s $MO  python3 -u main.py graph06 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph06.log
runlim -r $TO -s $MO  python3 -u main.py graph07 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph07.log
runlim -r $TO -s $MO  python3 -u main.py graph10 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph10.log
runlim -r $TO -s $MO  python3 -u main.py graph11 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph11.log
runlim -r $TO -s $MO  python3 -u main.py graph12 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph12.log
runlim -r $TO -s $MO  python3 -u main.py graph13 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph13.log
runlim -r $TO -s $MO  python3 -u main.py scen05 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen05.log
runlim -r $TO -s $MO  python3 -u main.py scen06 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen06.log
runlim -r $TO -s $MO  python3 -u main.py scen07 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen07.log
runlim -r $TO -s $MO  python3 -u main.py scen08 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen08.log
runlim -r $TO -s $MO  python3 -u main.py scen09 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen09.log
runlim -r $TO -s $MO  python3 -u main.py scen10 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen10.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.1 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.1.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.2 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.2.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.3 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.3.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.4 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.4.log
runlim -r $TO -s $MO  python3 -u main.py TUD200.5 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.5.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.1 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.1.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.2 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.2.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.3 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.3.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.4 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.4.log
runlim -r $TO -s $MO  python3 -u main.py TUD916.5 tot incremental cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.5.log
