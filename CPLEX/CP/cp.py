# cp.py
import os
import sys
import psutil
from time import time
from docplex.cp.model import CpoModel




def get_file_names(dataset_folder):
    base = os.path.basename(dataset_folder)
    if base.lower().startswith(("graph", "tud")):
        return {
            "domain": os.path.join(dataset_folder, "dom.txt"),
            "var": os.path.join(dataset_folder, "var.txt"),
            "ctr": os.path.join(dataset_folder, "ctr.txt")
        }
    elif base.lower().startswith("scen"):
        return {
            "domain": os.path.join(dataset_folder, "DOM.TXT"),
            "var": os.path.join(dataset_folder, "VAR.TXT"),
            "ctr": os.path.join(dataset_folder, "CTR.TXT")
        }
    else:
        raise ValueError("Not a valid dataset: " + dataset_folder)

def read_domain(file):
    domain = []
    with open(file) as f:
        for line in f:
            if line.strip() == '\x00':
                continue
            parts = line.strip().split()
            if not parts:
                continue
            values = list(map(int, parts[2:]))
            domain.append(values)
    return domain 

def read_var(file, domain):
    var = {}
    with open(file) as f:
        for line in f:
            if line.strip() == '\x00':
                continue
            parts = line.strip().split()
            if not parts:
                continue
            idx = int(parts[0])
            if len(parts) >= 4:
                var[idx] = [int(parts[-2])]
            else:
                var[idx] = domain[int(parts[1])]
    return var

def create_var_map(var):
    var_map = {}
    for i, vals in var.items():
        for v in vals:
            name = f"x_{i}_{v}"
            var_map[(i, v)] = name
    return var_map

def build_cp_model(var, var_map, ctr_file):
    mdl = CpoModel()

    # tạo biến x_{i,v}
    x_vars = {}
    for (i,v) in var_map.keys():
        x_vars[(i,v)] = mdl.binary_var(name=f"x_{i}_{v}")

    # mỗi node chọn đúng 1 label
    for i, vals in var.items():
        mdl.add(mdl.sum(x_vars[(i,v)] for v in vals) == 1)

    # distance constraints
    with open(ctr_file) as f:
        for line in f:
            if line.strip() == '\x00':
                continue
            parts = line.strip().split()
            if not parts:
                continue
            i, j = int(parts[0]), int(parts[1])
            vals_i = var.get(i, [])
            vals_j = var.get(j, [])
            distance = int(parts[4])
            if '>' in parts:
                # |vi - vj| > distance
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) <= distance:
                            mdl.add(x_vars[(i,vi)] + x_vars[(j,vj)] <= 1)
            elif '=' in parts:
                # |vi - vj| == distance
                for vi in vals_i:
                    allowed = [vj for vj in vals_j if abs(vi - vj) == distance]
                    if allowed:
                        mdl.add(x_vars[(i,vi)] <= mdl.sum(x_vars[(j,vj)] for vj in allowed))
                for vj in vals_j:
                    allowed = [vi for vi in vals_i if abs(vi - vj) == distance]
                    if allowed:
                        mdl.add(x_vars[(j,vj)] <= mdl.sum(x_vars[(i,vi)] for vi in allowed))

    all_labels = set()
    for vals in var.values():
        all_labels.update(vals)

    l_vars = {}
    for v in all_labels:
        l_vars[v] = mdl.binary_var(name=f"l_{v}")

    # liên kết x_{i,v} <= l_v
    for (i,v), var_obj in x_vars.items():
        mdl.add(var_obj <= l_vars[v])

    mdl.add(mdl.minimize(mdl.sum(l_vars[v] for v in all_labels)))

    return mdl, x_vars

def main():
    start_time = time()
    if len(sys.argv) < 2:
        print("Use: python cp.py <dataset_folder>")
        return

    dataset_folder = os.path.join("dataset", sys.argv[1])

    try:
        files = get_file_names(dataset_folder)
    except ValueError as e:
        print(e)
        return

    domain = read_domain(files["domain"])
    var = read_var(files["var"], domain)
    var_map = create_var_map(var)

    print("Building CP model...")
    build_start = time()
    mdl, x_vars = build_cp_model(var, var_map, files["ctr"])
    print(f"Build time: {time() - build_start:.2f}s")



    print("Solving CP Optimizer...")
    solver = mdl.create_solver(LogVerbosity="Terse")
    result = solver.solve()

    if result is None:
        print("No solution found.")
        return

    status = result.get_solve_status()
    if status not in ("Optimal", "Feasible"):
        print("No valid solution:", status)
        return

    assignment = {}
    for (i,v), var_obj in x_vars.items():
        if result.get_value(var_obj) >= 0.5:
            assignment[i] = v

    print("\nFINAL SOLUTION:")
    print("{" + ", ".join(f"{v}" for i, v in sorted(assignment.items())) + "}")
    print("Number of labels used:", len(set(assignment.values())))


if __name__ == "__main__":
    main()
