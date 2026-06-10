TO=600
MO=14000

RESULTS_DIR=results/no_processing/DSE/ladder
mkdir -p $RESULTS_DIR


./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen01 DSE 6  2>&1 | tee $RESULTS_DIR/scen01.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen02 DSE 6  2>&1 | tee $RESULTS_DIR/scen02.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen03 DSE 6  2>&1 | tee $RESULTS_DIR/scen03.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen04 DSE 6  2>&1 | tee $RESULTS_DIR/scen04.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen11 DSE 6  2>&1 | tee $RESULTS_DIR/scen11.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph01 DSE 6  2>&1 | tee $RESULTS_DIR/graph01.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph02 DSE 6  2>&1 | tee $RESULTS_DIR/graph02.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph08 DSE 6  2>&1 | tee $RESULTS_DIR/graph08.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph09 DSE 6  2>&1 | tee $RESULTS_DIR/graph09.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph14 DSE 6  2>&1 | tee $RESULTS_DIR/graph14.log

./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph03 DSE 6  2>&1 | tee $RESULTS_DIR/graph03.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph04 DSE 6  2>&1 | tee $RESULTS_DIR/graph04.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph05 DSE 6  2>&1 | tee $RESULTS_DIR/graph05.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph06 DSE 6  2>&1 | tee $RESULTS_DIR/graph06.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph07 DSE 6  2>&1 | tee $RESULTS_DIR/graph07.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph10 DSE 6  2>&1 | tee $RESULTS_DIR/graph10.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph11 DSE 6  2>&1 | tee $RESULTS_DIR/graph11.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph12 DSE 6  2>&1 | tee $RESULTS_DIR/graph12.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py graph13 DSE 6  2>&1 | tee $RESULTS_DIR/graph13.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen05 DSE 6  2>&1 | tee $RESULTS_DIR/scen05.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen06 DSE 6  2>&1 | tee $RESULTS_DIR/scen06.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen07 DSE 6  2>&1 | tee $RESULTS_DIR/scen07.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen08 DSE 6  2>&1 | tee $RESULTS_DIR/scen08.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen09 DSE 6  2>&1 | tee $RESULTS_DIR/scen09.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py scen10 DSE 6  2>&1 | tee $RESULTS_DIR/scen10.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD200.1 DSE 6  2>&1 | tee $RESULTS_DIR/TUD200.1.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD200.2 DSE 6  2>&1 | tee $RESULTS_DIR/TUD200.2.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD200.3 DSE 6  2>&1 | tee $RESULTS_DIR/TUD200.3.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD200.4 DSE 6  2>&1 | tee $RESULTS_DIR/TUD200.4.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD200.5 DSE 6  2>&1 | tee $RESULTS_DIR/TUD200.5.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD916.1 DSE 6  2>&1 | tee $RESULTS_DIR/TUD916.1.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD916.2 DSE 6  2>&1 | tee $RESULTS_DIR/TUD916.2.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD916.3 DSE 6  2>&1 | tee $RESULTS_DIR/TUD916.3.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD916.4 DSE 6  2>&1 | tee $RESULTS_DIR/TUD916.4.log
./runlim -r $TO -s $MO  python3 -u main_no_processing.py TUD916.5 DSE 6  2>&1 | tee $RESULTS_DIR/TUD916.5.log
