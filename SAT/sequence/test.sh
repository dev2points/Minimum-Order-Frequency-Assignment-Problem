TO=70
MO=14000
RESULTS_DIR=result_test
mkdir -p $RESULTS_DIR


runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions cadical103 2>&1 | tee $RESULTS_DIR/graph08_cadical103.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions cadical103 2>&1 | tee $RESULTS_DIR/graph09_cadical103.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions cadical153 2>&1 | tee $RESULTS_DIR/graph08_cadical153.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions cadical153 2>&1 | tee $RESULTS_DIR/graph09_cadical153.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions cadical195 2>&1 | tee $RESULTS_DIR/graph08_cadical195.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions cadical195 2>&1 | tee $RESULTS_DIR/graph09_cadical195.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions cryptominisat 2>&1 | tee $RESULTS_DIR/graph08_cryptominisat.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions cryptominisat 2>&1 | tee $RESULTS_DIR/graph09_cryptominisat.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions gluecard3 2>&1 | tee $RESULTS_DIR/graph08_gluecard3.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions gluecard3 2>&1 | tee $RESULTS_DIR/graph09_gluecard3.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions gluecard4 2>&1 | tee $RESULTS_DIR/graph08_gluecard4.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions gluecard4 2>&1 | tee $RESULTS_DIR/graph09_gluecard4.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions glucose4 2>&1 | tee $RESULTS_DIR/graph08_glucose4.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions glucose4 2>&1 | tee $RESULTS_DIR/graph09_glucose4.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions glucose3 2>&1 | tee $RESULTS_DIR/graph08_glucose3.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions glucose3 2>&1 | tee $RESULTS_DIR/graph09_glucose3.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions glucose4 2>&1 | tee $RESULTS_DIR/graph08_glucose4.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions glucose4 2>&1 | tee $RESULTS_DIR/graph09_glucose4.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions glucose42 2>&1 | tee $RESULTS_DIR/graph08_glucose42.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions glucose42 2>&1 | tee $RESULTS_DIR/graph09_glucose42.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions lingeling 2>&1 | tee $RESULTS_DIR/graph08_lingeling.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions lingeling 2>&1 | tee $RESULTS_DIR/graph09_lingeling.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions maplechrono 2>&1 | tee $RESULTS_DIR/graph08_maplechrono.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions maplechrono 2>&1 | tee $RESULTS_DIR/graph09_maplechrono.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions maplecm 2>&1 | tee $RESULTS_DIR/graph08_maplecm.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions maplecm 2>&1 | tee $RESULTS_DIR/graph09_maplecm.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions maplesat 2>&1 | tee $RESULTS_DIR/graph08_maplesat.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions maplesat 2>&1 | tee $RESULTS_DIR/graph09_maplesat.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions mergesat3 2>&1 | tee $RESULTS_DIR/graph08_mergesat3.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions mergesat3 2>&1 | tee $RESULTS_DIR/graph09_mergesat3.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions minicard 2>&1 | tee $RESULTS_DIR/graph08_minicard.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions minicard 2>&1 | tee $RESULTS_DIR/graph09_minicard.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions minisat22 2>&1 | tee $RESULTS_DIR/graph08_minisat22.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions minisat22 2>&1 | tee $RESULTS_DIR/graph09_minisat22.log

runlim -r $TO -s $MO  python3 -u main.py graph08 sc_reduced assumptions minisatgh 2>&1 | tee $RESULTS_DIR/graph08_minisatgh.log
runlim -r $TO -s $MO  python3 -u main.py graph09 nsc assumptions minisatgh 2>&1 | tee $RESULTS_DIR/graph09_minisatgh.log
