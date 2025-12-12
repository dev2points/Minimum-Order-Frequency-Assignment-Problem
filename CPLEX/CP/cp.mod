using CPLEX;

// Sets
int NODES = ...; // số lượng nodes
int LABELS = ...; // số lượng labels
range Nodes = 1..NODES;
range Labels = 1..LABELS;

// Domain của mỗi node 
{int} domain[Nodes] = ...; // đọc từ file domain hoặc định nghĩa trực tiếp

// Các ràng buộc khoảng cách
tuple DistanceConstraint {
    int i;
    int j;
    string type; 
    int value;
}
{DistanceConstraint} ctr = ...;

// x[i,v] = 1 nếu node i được gán label v
dvar boolean x[Nodes][Labels];

// l[v] = 1 nếu label v được sử dụng
dvar boolean l[Labels];

minimize sum(v in Labels) l[v];

subject to {
    forall(i in Nodes)
        sum(v in domain[i]) x[i][v] == 1;
}

subject to {
    forall(i in Nodes, v in domain[i])
        x[i][v] <= l[v];
}

subject to {
    forall(c in ctr) {
        if(c.type == ">") {
            // không được có |vi - vj| <= value
            forall(vi in domain[c.i], vj in domain[c.j] : abs(vi - vj) <= c.value)
                x[c.i][vi] + x[c.j][vj] <= 1;
        }
        else if (c.type == "=") {

            // Hướng i -> j
            forall(vi in domain[c.i]) {

                // xem có label j nào hợp lệ hay không
                if (sum(vj in domain[c.j] : abs(vi - vj) == c.value) 1 > 0)
                    x[c.i][vi] <= sum(vj in domain[c.j] : abs(vi - vj) == c.value) x[c.j][vj];
                else
                    x[c.i][vi] == 0;
            }

            // Hướng j -> i
            forall(vj in domain[c.j]) {

                if (sum(vi in domain[c.i] : abs(vi - vj) == c.value) 1 > 0)
                    x[c.j][vj] <= sum(vi in domain[c.i] : abs(vi - vj) == c.value) x[c.i][vi];
                else
                    x[c.j][vj] == 0;
            }
        }
    }
}

