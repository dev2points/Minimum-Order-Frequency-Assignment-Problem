TO=600
MO=14000

RESULTS_DIR=results/processing/totalizer
mkdir -p $RESULTS_DIR


./runlim -r $TO -s $MO  python3 -u main.py scen01 assumptions 5  2>&1 | tee $RESULTS_DIR/scen01.log
./runlim -r $TO -s $MO  python3 -u main.py scen02 assumptions 5  2>&1 | tee $RESULTS_DIR/scen02.log
./runlim -r $TO -s $MO  python3 -u main.py scen03 assumptions 5  2>&1 | tee $RESULTS_DIR/scen03.log
./runlim -r $TO -s $MO  python3 -u main.py scen04 assumptions 5  2>&1 | tee $RESULTS_DIR/scen04.log
./runlim -r $TO -s $MO  python3 -u main.py scen11 assumptions 5  2>&1 | tee $RESULTS_DIR/scen11.log
./runlim -r $TO -s $MO  python3 -u main.py graph01 assumptions 5  2>&1 | tee $RESULTS_DIR/graph01.log
./runlim -r $TO -s $MO  python3 -u main.py graph02 assumptions 5  2>&1 | tee $RESULTS_DIR/graph02.log
./runlim -r $TO -s $MO  python3 -u main.py graph08 assumptions 5  2>&1 | tee $RESULTS_DIR/graph08.log
./runlim -r $TO -s $MO  python3 -u main.py graph09 assumptions 5  2>&1 | tee $RESULTS_DIR/graph09.log
./runlim -r $TO -s $MO  python3 -u main.py graph14 assumptions 5  2>&1 | tee $RESULTS_DIR/graph14.log

./runlim -r $TO -s $MO  python3 -u main.py graph03 assumptions 5  2>&1 | tee $RESULTS_DIR/graph03.log
./runlim -r $TO -s $MO  python3 -u main.py graph04 assumptions 5  2>&1 | tee $RESULTS_DIR/graph04.log
./runlim -r $TO -s $MO  python3 -u main.py graph05 assumptions 5  2>&1 | tee $RESULTS_DIR/graph05.log
./runlim -r $TO -s $MO  python3 -u main.py graph06 assumptions 5  2>&1 | tee $RESULTS_DIR/graph06.log
./runlim -r $TO -s $MO  python3 -u main.py graph07 assumptions 5  2>&1 | tee $RESULTS_DIR/graph07.log
./runlim -r $TO -s $MO  python3 -u main.py graph10 assumptions 5  2>&1 | tee $RESULTS_DIR/graph10.log
./runlim -r $TO -s $MO  python3 -u main.py graph11 assumptions 5  2>&1 | tee $RESULTS_DIR/graph11.log
./runlim -r $TO -s $MO  python3 -u main.py graph12 assumptions 5  2>&1 | tee $RESULTS_DIR/graph12.log
./runlim -r $TO -s $MO  python3 -u main.py graph13 assumptions 5  2>&1 | tee $RESULTS_DIR/graph13.log
./runlim -r $TO -s $MO  python3 -u main.py scen05 assumptions 5  2>&1 | tee $RESULTS_DIR/scen05.log
./runlim -r $TO -s $MO  python3 -u main.py scen06 assumptions 5  2>&1 | tee $RESULTS_DIR/scen06.log
./runlim -r $TO -s $MO  python3 -u main.py scen07 assumptions 5  2>&1 | tee $RESULTS_DIR/scen07.log
./runlim -r $TO -s $MO  python3 -u main.py scen08 assumptions 5  2>&1 | tee $RESULTS_DIR/scen08.log
./runlim -r $TO -s $MO  python3 -u main.py scen09 assumptions 5  2>&1 | tee $RESULTS_DIR/scen09.log
./runlim -r $TO -s $MO  python3 -u main.py scen10 assumptions 5  2>&1 | tee $RESULTS_DIR/scen10.log
./runlim -r $TO -s $MO  python3 -u main.py TUD200.1 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD200.1.log
./runlim -r $TO -s $MO  python3 -u main.py TUD200.2 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD200.2.log
./runlim -r $TO -s $MO  python3 -u main.py TUD200.3 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD200.3.log
./runlim -r $TO -s $MO  python3 -u main.py TUD200.4 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD200.4.log
./runlim -r $TO -s $MO  python3 -u main.py TUD200.5 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD200.5.log
./runlim -r $TO -s $MO  python3 -u main.py TUD916.1 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD916.1.log
./runlim -r $TO -s $MO  python3 -u main.py TUD916.2 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD916.2.log
./runlim -r $TO -s $MO  python3 -u main.py TUD916.3 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD916.3.log
./runlim -r $TO -s $MO  python3 -u main.py TUD916.4 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD916.4.log
./runlim -r $TO -s $MO  python3 -u main.py TUD916.5 assumptions 5  2>&1 | tee $RESULTS_DIR/TUD916.5.log
