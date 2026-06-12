# OR-Tools CP-SAT CP-style model

This folder is intended for a CP-SAT-native formulation of MO-FAP.

Unlike `../CPSAT`, which uses the binary MIP/PBO-style formulation with
`x_{i,v}` and `y_v`, this variant should use one integer-domain variable
`f_i` per transmitter:

```text
f_i in D_i
```

Distance constraints are represented directly through absolute differences:

```text
abs(f_i - f_j) > d
abs(f_i - f_j) = d
```

The objective still minimizes the number of used labels. This requires label
usage Booleans `y_l` and channel-value indicator Booleans linking `f_i == l`
to `y_l`.

This formulation is less directly comparable to Gurobi/CPLEX MIP than
`../CPSAT`, but it is more CP-SAT-native.

## Run

```bash
python main.py graph04 600
python main_no.py graph04 600
```

`main.py` uses preprocessing; `main_no.py` does not.
