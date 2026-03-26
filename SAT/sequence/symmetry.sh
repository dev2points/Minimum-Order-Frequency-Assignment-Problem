TO=600
MO=14000

ASSUMPTIONS_RESULT=results/symmetry/assumptions
mkdir -p $ASSUMPTIONS_RESULT

INCREMENTAL_RESULT=results/symmetry/incremental
mkdir -p $INCREMENTAL_RESULT


./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen01 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen01.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen02 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen02.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen03 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen03.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen04 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen04.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen11 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen11.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph01 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph01.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph02 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph02.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph08 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph08.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph09 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph09.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph14 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph14.log

./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph03 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph03.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph04 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph04.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph05 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph05.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph06 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph06.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph07 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph07.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph10 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph10.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph11 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph11.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph12 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph12.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph13 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/graph13.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen05 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen05.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen06 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen06.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen07 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen07.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen08 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen08.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen09 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen09.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen10 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/scen10.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.1 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.1.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.2 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.2.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.3 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.3.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.4 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.4.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.5 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.5.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.1 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.1.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.2 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.2.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.3 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.3.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.4 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.4.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.5 nsc assumptions cadical195 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.5.log

./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen01 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen01.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen02 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen02.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen03 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen03.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen04 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen04.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen11 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen11.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph01 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph01.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph02 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph02.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph08 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph08.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph09 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph09.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph14 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph14.log

./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph03 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph03.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph04 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph04.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph05 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph05.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph06 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph06.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph07 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph07.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph10 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph10.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph11 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph11.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph12 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph12.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py graph13 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/graph13.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen05 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen05.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen06 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen06.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen07 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen07.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen08 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen08.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen09 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen09.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py scen10 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/scen10.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.1 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD200.1.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.2 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD200.2.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.3 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD200.3.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.4 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD200.4.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD200.5 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD200.5.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.1 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD916.1.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.2 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD916.2.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.3 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD916.3.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.4 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD916.4.log
./runlim -r $TO -s $MO  python3 -u main_symmetry.py TUD916.5 nsc incremental cadical195 2>&1 | tee $INCREMENTAL_RESULT/TUD916.5.log
