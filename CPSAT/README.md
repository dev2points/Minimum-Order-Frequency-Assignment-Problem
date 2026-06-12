# OR-Tools CP-SAT model

This folder contains an OR-Tools CP-SAT formulation for MO-FAP.

The model uses binary assignment variables `x_{i,v}`, binary label usage variables
`y_v`, exactly-one assignment constraints, label-linking constraints `x_{i,v} <= y_v`,
the original distance/equality constraints, and objective `min sum_v y_v`.

## Install

```bash
pip install -r requirements.txt
```

## Run

With preprocessing:

```bash
python main.py graph04
```

Without preprocessing:

```bash
python main_no.py graph04
```

With a time limit in seconds:

```bash
python main.py graph04 600
python main_no.py graph04 600
```

The script looks for datasets in `CPSAT/dataset`, then `../Gurobi/dataset`,
then `../SAT/pairwise/dataset`.
