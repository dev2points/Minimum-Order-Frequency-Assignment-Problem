import os
import psutil
import sys
from time import time
from pysat.solvers import Solver
from pypblib import pblib

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
            if len(parts) >= 4:
                var[idx] = [int(parts[-2])]
            else:
                var[idx] = domain[int(parts[1])]
    return var # domain subset for each variable
def delete_invalid_labels(var, ctr_file):
    # Read constraints and remove invalid labels from domain
    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            u, v = int(parts[0]), int(parts[1])
            distance = int(parts[4])
            if '>' in parts:
                var[u] = [label for label in var[u] if any(abs(label - label_v) > distance for label_v in var[v])] 
                var[v] = [label for label in var[v] if any(abs(label - label_u) > distance for label_u in var[u])]
    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            u, v = int(parts[0]), int(parts[1])
            distance = int(parts[4])
            if '=' in parts:
                # Remove labels from domain that violate the equality constraint
                var[u] = [label for label in var[u] if any(abs(label - label_v) == distance for label_v in var[v])] 
                var[v] = [label for label in var[v] if any(abs(label - label_u) == distance for label_u in var[u])]

def create_var_map(var):
    var_map = {}
    counter = 0
    for i, vals in var.items():
        for v in vals:
            counter += 1
            var_map[(i, v)] = counter
            
    return counter, var_map # dict mapping (i, v) to variable number

def create_order_var_map(var,var_map, last_var_num, solver):
    counter = last_var_num + 1
    order_var_map = {}

    for u, labels in var.items():
        for i in labels:
            order_var_map[(u,i)] = counter
            counter += 1             
    return order_var_map # dict mapping (u,i) to order variable number

def build_constraints(solver, var, var_map, ctr_file):
    # Exactly One
    for i, vals in var.items():
        solver.add_clause([var_map[(i, v)] for v in vals])
        for j in range(len(vals)):
            for k in range(j+1, len(vals)):
                solver.add_clause([-var_map[(i, vals[j])], -var_map[(i, vals[k])]])

    # Distance constraints
    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            i, j = int(parts[0]), int(parts[1])
            vals_i = var.get(i, [])
            vals_j = var.get(j, [])
            if '>' in parts:
                distance = int(parts[4])
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) <= distance:
                            solver.add_clause([-var_map[(i, vi)], -var_map[(j, vj)]])
                            
            elif '=' in parts:
                target = int(parts[4])
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) == target:
                            solver.add_clause([-var_map[(i, vi)], var_map[(j, vj)]])
    

    
    
                            
def create_label_var_map(labels, start_index):
    label_var_map = {}
    current = start_index
    for lb in labels:
        label_var_map[lb] = current
        current += 1
    return label_var_map
    
# ánh xạ biến active -> biến xác nhận label được sử dụng    
def build_label_constraints(solver, var_map, label_var_map):
    for (i, v), varnum in var_map.items():
        lb_varnum = label_var_map[v]
        solver.add_clause([-varnum, lb_varnum])

def add_limit_label_constraints(solver, label_var_map, UB):
    first_free_var = solver.nof_vars() 
    x_vars = []
    for i in range(UB):
        first_free_var += 1
        x_vars.append(first_free_var)

    for i in range(UB - 1):
        solver.add_clause([-x_vars[i], x_vars[i + 1]])

    label_vars = list(label_var_map.values())
    label_vars.extend(x_vars)

    config = pblib.PBConfig()
    pb2 = pblib.Pb2cnf(config)
    formular = []
    atmost_k = pb2.encode_leq([1]*len(label_vars), label_vars, UB, formular,solver.nof_vars() +1)

    for clause in formular:
        solver.add_clause(clause)
    return x_vars


def solve_and_print(solver, var_map):
    if solver.solve():
        model = solver.get_model()
        assignment = {}
        for (i, v), varnum in var_map.items():
            if model[varnum-1] > 0:
                assignment[i] = v
        print("Solution:")
        # print("{" + ", ".join(f"{v}" for i, v in sorted(assignment.items())) + "}")
        print(assignment)
        return assignment
    else:
        print("Cannot find solution.")
        return None

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
            if(vi not in var[i]) or (vj not in var[j]):
                return False
            if '>' in parts:
                distance = int(parts[4])
                if abs(vi - vj) <= distance:
                    return False
            elif '=' in parts:
                value = int(parts[4])
                if abs(vi - vj) != value:
                    return False
    return True

def main():
    start_time = time()
    if len(sys.argv) < 2:
        print("Use: python main.py <dataset_folder>")
        return

    dataset_folder = os.path.join("dataset", sys.argv[1])

    try:
        files = get_file_names(dataset_folder)
    except ValueError as e:
        print(e)
        return

    domain = read_domain(files["domain"])
    var = read_var(files["var"], domain)
    #delete_invalid_labels(var, files["ctr"])
    solver = Solver(name='glucose4')
    last_var_num, var_map = create_var_map(var)

    print("Solve first problem:")
    
    # solver = Cadical195()
    build_constraints(solver, var, var_map, files["ctr"])

    assignment = solve_and_print(solver, var_map)
    if assignment is None:
        return
    if verify_solution_simple(assignment, var, files["ctr"]):
        print("Correct solution!")
        num_lables = len(set(assignment.values()))
        print("Number of lables used: ", num_lables)
    else:   
        print("Incorrect solution!")
        return
    print(f"Total time: {time() - start_time:.2f} seconds")
    process = psutil.Process(os.getpid())
    print(f"Memory used: {process.memory_info().rss / 1024**2:.2f} MB")
    lable_var_map = create_label_var_map(domain[0], solver.nof_vars() + 1)
    build_label_constraints(solver, var_map, lable_var_map)
    x_vars = add_limit_label_constraints(solver, lable_var_map,num_lables)

    

    while num_lables > 1:
        
        print("--------------------------------------------------")
        print(f"\nTrying with at most {num_lables - 1} labels...")
        solver.add_clause([x_vars[num_lables - 1]])
        assignment = solve_and_print(solver, var_map)
        if assignment is None:
            print("No more solutions found.")
            print("Optimal number of labels used: ", num_lables)
            print(f"Total time: {time() - start_time:.2f} seconds")
            process = psutil.Process(os.getpid())
            print(f"Memory used: {process.memory_info().rss / 1024**2:.2f} MB")
            
            break
        if verify_solution_simple(assignment, var, files["ctr"]):
            print("Correct solution!")
        else:
            print("Incorrect solution!")
            break
        new_num_lables = len(set(assignment.values()))
        print("Number of lables used: ", new_num_lables)
        num_lables = new_num_lables

        print(f"Total time: {time() - start_time:.2f} seconds")
        process = psutil.Process(os.getpid())
        print(f"Memory used: {process.memory_info().rss / 1024**2:.2f} MB")

    solver.delete()

if __name__ == "__main__":
    main()
