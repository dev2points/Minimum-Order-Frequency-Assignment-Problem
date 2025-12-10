TO=600
MO=3000
RESULTS_DIR=results
mkdir -p $RESULTS_DIR


runlim -r $TO -s $MO  python3 -u mip.py $TO graph01  2>&1 | tee $RESULTS_DIR/graph01.log
runlim -r $TO -s $MO  python3 -u mip.py $TO graph02  2>&1 | tee $RESULTS_DIR/graph02.log
runlim -r $TO -s $MO  python3 -u mip.py $TO graph08  2>&1 | tee $RESULTS_DIR/graph08.log
runlim -r $TO -s $MO  python3 -u mip.py $TO graph09  2>&1 | tee $RESULTS_DIR/graph09.log
runlim -r $TO -s $MO  python3 -u mip.py $TO graph14  2>&1 | tee $RESULTS_DIR/graph14.log
runlim -r $TO -s $MO  python3 -u mip.py $TO scen01  2>&1 | tee $RESULTS_DIR/scen01.log
runlim -r $TO -s $MO  python3 -u mip.py $TO scen02  2>&1 | tee $RESULTS_DIR/scen02.log
runlim -r $TO -s $MO  python3 -u mip.py $TO scen03  2>&1 | tee $RESULTS_DIR/scen03.log
runlim -r $TO -s $MO  python3 -u mip.py $TO scen04  2>&1 | tee $RESULTS_DIR/scen04.log
runlim -r $TO -s $MO  python3 -u mip.py $TO scen11  2>&1 | tee $RESULTS_DIR/scen11.log
