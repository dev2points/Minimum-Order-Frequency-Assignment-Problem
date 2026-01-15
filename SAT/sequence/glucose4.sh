TO=900
MO=8000
BDD_RESULTS_DI=results/glucose4/pb_bdd
BINARY_MERGE_RESULTS_DI=results/glucose4/pb_binary_merge
SEQ_RESULTS_DI=results/glucose4/card_seq
CARDNET_RESULTS_DI=results/glucose4/card_cardnet
mkdir -p $BDD_RESULTS_DI
mkdir -p $BINARY_MERGE_RESULTS_DI
mkdir -p $SEQ_RESULTS_DI
mkdir -p $CARDNET_RESULTS_DI



runlim -r $TO -s $MO  python3 -u pb.py scen01 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/scen01.log
runlim -r $TO -s $MO  python3 -u pb.py scen02 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/scen02.log
runlim -r $TO -s $MO  python3 -u pb.py scen03 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/scen03.log
runlim -r $TO -s $MO  python3 -u pb.py scen04 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/scen04.log
runlim -r $TO -s $MO  python3 -u pb.py scen11 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/scen11.log
runlim -r $TO -s $MO  python3 -u pb.py graph01 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/graph01.log
runlim -r $TO -s $MO  python3 -u pb.py graph02 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/graph02.log
runlim -r $TO -s $MO  python3 -u pb.py graph08 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/graph08.log
runlim -r $TO -s $MO  python3 -u pb.py graph09 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/graph09.log
runlim -r $TO -s $MO  python3 -u pb.py graph14 pb_bdd glucose4 2>&1 | tee $BDD_RESULTS_DI/graph14.log

runlim -r $TO -s $MO  python3 -u pb.py scen01 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/scen01.log
runlim -r $TO -s $MO  python3 -u pb.py scen02 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/scen02.log
runlim -r $TO -s $MO  python3 -u pb.py scen03 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/scen03.log
runlim -r $TO -s $MO  python3 -u pb.py scen04 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/scen04.log
runlim -r $TO -s $MO  python3 -u pb.py scen11 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/scen11.log
runlim -r $TO -s $MO  python3 -u pb.py graph01 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/graph01.log
runlim -r $TO -s $MO  python3 -u pb.py graph02 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/graph02.log
runlim -r $TO -s $MO  python3 -u pb.py graph08 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/graph08.log
runlim -r $TO -s $MO  python3 -u pb.py graph09 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/graph09.log
runlim -r $TO -s $MO  python3 -u pb.py graph14 pb_binary_merge glucose4 2>&1 | tee $BINARY_MERGE_RESULTS_DI/graph14.log

runlim -r $TO -s $MO  python3 -u pb.py scen01 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/scen01.log
runlim -r $TO -s $MO  python3 -u pb.py scen02 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/scen02.log
runlim -r $TO -s $MO  python3 -u pb.py scen03 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/scen03.log
runlim -r $TO -s $MO  python3 -u pb.py scen04 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/scen04.log
runlim -r $TO -s $MO  python3 -u pb.py scen11 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/scen11.log
runlim -r $TO -s $MO  python3 -u pb.py graph01 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/graph01.log
runlim -r $TO -s $MO  python3 -u pb.py graph02 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/graph02.log
runlim -r $TO -s $MO  python3 -u pb.py graph08 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/graph08.log
runlim -r $TO -s $MO  python3 -u pb.py graph09 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/graph09.log
runlim -r $TO -s $MO  python3 -u pb.py graph14 card_seq glucose4 2>&1 | tee $SEQ_RESULTS_DI/graph14.log

runlim -r $TO -s $MO  python3 -u pb.py scen01 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/scen01.log
runlim -r $TO -s $MO  python3 -u pb.py scen02 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/scen02.log
runlim -r $TO -s $MO  python3 -u pb.py scen03 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/scen03.log
runlim -r $TO -s $MO  python3 -u pb.py scen04 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/scen04.log
runlim -r $TO -s $MO  python3 -u pb.py scen11 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/scen11.log
runlim -r $TO -s $MO  python3 -u pb.py graph01 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/graph01.log
runlim -r $TO -s $MO  python3 -u pb.py graph02 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/graph02.log
runlim -r $TO -s $MO  python3 -u pb.py graph08 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/graph08.log
runlim -r $TO -s $MO  python3 -u pb.py graph09 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/graph09.log
runlim -r $TO -s $MO  python3 -u pb.py graph14 card_cardnet glucose4 2>&1 | tee $CARDNET_RESULTS_DI/graph14.log

