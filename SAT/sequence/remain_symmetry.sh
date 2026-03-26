TO=600
MO=14000

CAD_RESULTS_DIR=results/remain_symmetry/nsc 
mkdir -p $CAD_RESULTS_DIR



./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen01 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen01.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen02 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen02.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen03 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen03.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen04 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen04.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen11 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen11.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph01 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph01.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph02 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph02.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph08 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph08.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph09 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph09.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph14 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph14.log

./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph03 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph03.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph04 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph04.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph05 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph05.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph06 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph06.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph07 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph07.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph10 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph10.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph11 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph11.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph12 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph12.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py graph13 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/graph13.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen05 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen05.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen06 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen06.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen07 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen07.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen08 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen08.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen09 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen09.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py scen10 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/scen10.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD200.1 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.1.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD200.2 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.2.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD200.3 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.3.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD200.4 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.4.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD200.5 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD200.5.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD916.1 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.1.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD916.2 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.2.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD916.3 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.3.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD916.4 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.4.log
./runlim -r $TO -s $MO  python3 -u remain_symmetry.py TUD916.5 nsc   cadical195 2>&1 | tee $CAD_RESULTS_DIR/TUD916.5.log