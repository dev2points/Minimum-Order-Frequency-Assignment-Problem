TO=600
MO=14000

ASSUMPTIONS_RESULT=results/tot_assumptions 
mkdir -p $ASSUMPTIONS_RESULT

INCREMENTAL_RESULT=results/tot_incremental 
mkdir -p $INCREMENTAL_RESULT


runlim -r $TO -s $MO  python3 -u pairwise.py scen01  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen01.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen02  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen02.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen03  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen03.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen04  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen04.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen11  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen11.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph01  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph01.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph02  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph02.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph08  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph08.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph09  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph09.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph14  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph14.log

runlim -r $TO -s $MO  python3 -u pairwise.py graph03  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph03.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph04  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph04.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph05  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph05.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph06  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph06.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph07  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph07.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph10  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph10.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph11  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph11.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph12  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph12.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph13  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/graph13.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen05  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen05.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen06  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen06.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen07  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen07.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen08  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen08.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen09  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen09.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen10  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/scen10.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.1  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.1.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.2  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.2.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.3  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.3.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.4  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.4.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.5  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD200.5.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.1  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.1.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.2  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.2.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.3  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.3.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.4  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.4.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.5  assumptions 2>&1 | tee $ASSUMPTIONS_RESULT/TUD916.5.log

runlim -r $TO -s $MO  python3 -u pairwise.py scen01  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen01.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen02  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen02.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen03  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen03.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen04  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen04.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen11  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen11.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph01  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph01.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph02  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph02.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph08  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph08.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph09  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph09.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph14  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph14.log

runlim -r $TO -s $MO  python3 -u pairwise.py graph03  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph03.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph04  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph04.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph05  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph05.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph06  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph06.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph07  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph07.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph10  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph10.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph11  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph11.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph12  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph12.log
runlim -r $TO -s $MO  python3 -u pairwise.py graph13  incremental 2>&1 | tee $INCREMENTAL_RESULT/graph13.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen05  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen05.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen06  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen06.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen07  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen07.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen08  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen08.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen09  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen09.log
runlim -r $TO -s $MO  python3 -u pairwise.py scen10  incremental 2>&1 | tee $INCREMENTAL_RESULT/scen10.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.1  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD200.1.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.2  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD200.2.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.3  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD200.3.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.4  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD200.4.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD200.5  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD200.5.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.1  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD916.1.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.2  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD916.2.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.3  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD916.3.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.4  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD916.4.log
runlim -r $TO -s $MO  python3 -u pairwise.py TUD916.5  incremental 2>&1 | tee $INCREMENTAL_RESULT/TUD916.5.log
