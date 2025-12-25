using CP;

// PARAMETERS
int LABELS = ...;

// Sets
{int} Nodes = ...;
range Labels = 1..LABELS;

// Domain cho mỗi node
{int} domain[Nodes] = ...;

// Distance constraints
tuple DistanceConstraint {
    int i;
    int j;
    string type;
    int value;
}
{DistanceConstraint} ctr = ...;

// Tách theo loại
{DistanceConstraint} ctrGreater = { c | c in ctr : c.type == ">" };
{DistanceConstraint} ctrEqual   = { c | c in ctr : c.type == "=" };

// Variables
dvar boolean x[Nodes][Labels];
dvar boolean l[Labels];

// Objective
minimize sum(v in Labels) l[v];

// 1 label per node
constraints {
    forall(i in Nodes)
        sum(v in domain[i]) x[i][v] == 1;
}

// x <= l
constraints {
    forall(i in Nodes, v in domain[i])
        x[i][v] <= l[v];
}

// TYPE ">"
constraints {
    forall(c in ctrGreater)
        forall(vi in domain[c.i], vj in domain[c.j] : abs(vi - vj) <= c.value)
            x[c.i][vi] + x[c.j][vj] <= 1;
}

// TYPE "="
constraints {
    forall(c in ctrEqual) {

        forall(vi in domain[c.i]) {
            if (sum(vj in domain[c.j] : abs(vi - vj) == c.value) 1 > 0)
                x[c.i][vi] <= sum(vj in domain[c.j] : abs(vi - vj) == c.value) x[c.j][vj];
            else
                x[c.i][vi] == 0;
        }

        forall(vj in domain[c.j]) {
            if (sum(vi in domain[c.i] : abs(vi - vj) == c.value) 1 > 0)
                x[c.j][vj] <= sum(vi in domain[c.i] : abs(vi - vj) == c.value) x[c.i][vi];
            else
                x[c.j][vj] == 0;
        }
    }
}
