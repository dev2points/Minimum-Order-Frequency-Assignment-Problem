# mip_cplex.py
import os
import sys
from time import time
import psutil
import cplex
from cplex.exceptions import CplexError

def get_file_names(dataset_folder):
    base = os.path.basename(dataset_folder)
    if base.lower().startswith("graph"):
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
            parts = line.strip().split()
            if not parts:
                continue
            idx = int(parts[0])
            subset_idx = int(parts[1])
            var[idx] = domain[subset_idx]
    return var # domain subset for each variable

def create_var_map(var):
    var_map = {}
    for i, vals in var.items():
        for v in vals:
            name = f"x_{i}_{v}"
            var_map[(i, v)] = name
    return var_map

def create_label_var_map(all_labels):
    label_var_map = {}
    for v in sorted(all_labels):
        label_var_map[v] = f"l_{v}"
    return label_var_map

def build_mip_model(var, var_map, label_var_map, ctr_file, time_limit = None):
    model = cplex.Cplex()
    try:
        model.parameters.timelimit.set(time_limit if time_limit is not None else 600)
    except Exception:
        pass

    # model.set_log_stream(None)
    # model.set_results_stream(None)
    # model.set_warning_stream(None)
    # model.set_error_stream(None)

    # Vertice-label variables
    x_names = [name for name in var_map.values()]
    # Label variables
    l_names = [name for name in label_var_map.values()]
    
    
    model.variables.add(names=x_names, types=[model.variables.type.binary]*len(x_names),
                        lb=[0.0]*len(x_names), ub=[1.0]*len(x_names))
    
    model.variables.add(names=l_names, types=[model.variables.type.binary]*len(l_names),
                        lb=[0.0]*len(l_names), ub=[1.0]*len(l_names))

    # Exactly one
    for i, vals in var.items():
        inds = [var_map[(i, v)] for v in vals]
        vals_coeff = [1.0]*len(inds)
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=inds, val=vals_coeff)],
            senses=["E"],
            rhs=[1.0]
        )

    # Link x_{i,v} <= l_v
    for (i, v), xname in var_map.items():
        lname = label_var_map[v]
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=[xname, lname], val=[1.0, -1.0])],
            senses=["L"],
            rhs=[0.0]
        )
        

    # Distance constraints 
    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            i, j = int(parts[0]), int(parts[1])
            vals_i = var.get(i, [])
            vals_j = var.get(j, [])
            try:
                distance = int(parts[-1])
            except:
                distance = int(parts[4])
            if '>' in parts:
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) <= distance:
                            model.linear_constraints.add(
                                lin_expr=[cplex.SparsePair(ind=[var_map[(i,vi)], var_map[(j,vj)]],
                                                          val=[1.0, 1.0])],
                                senses=["L"],
                                rhs=[1.0]
                            )
            elif '=' in parts:
                for vi in vals_i:
                    allowed = [var_map[(j, vj)] for vj in vals_j if abs(vi - vj) == distance]
                    if allowed:
                        inds = [var_map[(i,vi)]] + allowed
                        coeffs = [1.0] + [-1.0]*len(allowed)
                        model.linear_constraints.add(
                            lin_expr=[cplex.SparsePair(ind=inds, val=coeffs)],
                            senses=["L"],
                            rhs=[0.0]
                        )
                for vj in vals_j:
                    allowed = [var_map[(i, vi)] for vi in vals_i if abs(vi - vj) == distance]
                    if allowed:
                        inds = [var_map[(j,vj)]] + allowed
                        coeffs = [1.0] + [-1.0]*len(allowed)
                        model.linear_constraints.add(
                            lin_expr=[cplex.SparsePair(ind=inds, val=coeffs)],
                            senses=["L"],
                            rhs=[0.0]
                        )

    # Objective: minimize sum of label variables
    obj_inds = l_names
    obj_coeffs = [1.0]*len(l_names)
    model.objective.set_sense(model.objective.sense.minimize)
    model.objective.set_linear(list(zip(obj_inds, obj_coeffs)))

    return model

def extract_assignment_from_solution(model, var, var_map):
    sol = {}
    try:
        vals = model.solution.get_values()
    except CplexError:
        return None
    # get mapping name -> index
    name_to_index = {n: i for i, n in enumerate(model.variables.get_names())}
    for (i, v), name in var_map.items():
        idx = name_to_index[name]
        if vals[idx] > 0.5:
            sol[i] = v
    return sol

def verify_solution_simple(assignment, var, ctr_file):
    if assignment is None:
        return False
    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            i, j = int(parts[0]), int(parts[1])
            if i not in assignment or j not in assignment:
                return False
            vi = assignment[i]
            vj = assignment[j]
            if (vi not in var[i]) or (vj not in var[j]):
                return False
            if '>' in parts:
                distance = int(parts[-1])
                if abs(vi - vj) <= distance:
                    return False
            elif '=' in parts:
                value = int(parts[-1])
                if abs(vi - vj) != value:
                    return False
    return True

def main():
    start_time = time()
    if len(sys.argv) < 3:
        print("Use: python mip.py TO <dataset_folder>")
        return

    dataset_folder = os.path.join("dataset", sys.argv[2])
    time_limit = int(sys.argv[1])

    try:
        files = get_file_names(dataset_folder)
    except ValueError as e:
        print(e)
        return

    domain = read_domain(files["domain"])
    var = read_var(files["var"], domain)
    var_map = create_var_map(var)

    # collect all label values
    all_labels = set()
    for vals in var.values():
        all_labels.update(vals)
    label_var_map = create_label_var_map(all_labels)

    print("Building MIP model...")
    build_start = time()
    model = build_mip_model(var, var_map, label_var_map, files["ctr"], time_limit)
    print(f"Build time: {time() - build_start:.2f}s")

    print("Solving MIP (minimizing number of labels)...")
    solve_start = time()
    model.solve()
    solve_time = time() - solve_start
    print(f"Solve time: {solve_time:.2f}s")

    assignment = extract_assignment_from_solution(model, var, var_map)
    if assignment is None:
        print("No solution found.")
        return

    print("Solution :")
    print("{" + ", ".join(f"{v}" for i, v in sorted(assignment.items())) + "}")

    if verify_solution_simple(assignment, var, files["ctr"]):
        print("Correct solution!")
    else:
        print("Incorrect solution!")

    # number of labels used
    used_labels = set(assignment.values())
    print("Number of labels used:", len(used_labels))
    # print("Labels used:", sorted(list(used_labels)))

    end_time = time()
    print(f"Total time: {end_time - start_time:.2f}s")
    proc = psutil.Process(os.getpid())
    print(f"Memory used: {proc.memory_info().rss / 1024**2:.2f} MB")

if __name__ == "__main__":
    main()
