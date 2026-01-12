import os
import psutil
import sys
from time import time
from pysat.solvers import Solver
from pypblib import pblib
from pysat.card import CardEnc, EncType

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
    counter = 1
    for i, vals in var.items():
        for v in vals:
            var_map[(i, v)] = counter
            counter += 1
    return counter, var_map # dict mapping (i, v) to variable number

def create_order_var_map(var,var_map, last_var_num, solver):
    counter = last_var_num + 1
    order_var_map = {}

    for u, labels in var.items():
        for i in labels:
            order_var_map[(u,i)] = counter
            counter += 1

    # Monotonicity constraints 
    for u, labels in var.items():
        #(1)
        last_i = labels[-1]
        solver.add_clause([-var_map[(u, last_i)], order_var_map[(u, last_i)]])   # x -> y
        solver.add_clause([-order_var_map[(u, last_i)], var_map[(u, last_i)]])   # y -> x
        for idx in range(1, len(labels)):
            solver.add_clause([-order_var_map[(u, labels[idx])], order_var_map[(u, labels[idx - 1])]]) #(4)
        solver.add_clause([order_var_map[(u, labels[0])]]) #(3)
        #(2)
        for idx in range(len(labels)-1):
            solver.add_clause([-var_map[(u, labels[idx])], order_var_map[(u, labels[idx])]])
            solver.add_clause([-var_map[(u, labels[idx])], -order_var_map[(u, labels[idx + 1])]])  
            solver.add_clause([-order_var_map[(u, labels[idx])], order_var_map[(u, labels[idx + 1])], var_map[(u, labels[idx])]])
                

    

    return order_var_map # dict mapping (u,i) to order variable number

def build_constraints(solver, var, var_map, last_var_num, ctr_file):

    # Order encoding of distance constraints
    order_var_map = create_order_var_map(var,var_map,last_var_num, solver)

    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            u, v = int(parts[0]), int(parts[1])
            vals_u = var.get(u, [])
            vals_v = var.get(v, [])
            distance = int(parts[4])
            if '=' in parts:
                for iu in vals_u:
                    for jv in vals_v:
                        if abs(iu - jv) == distance:
                            solver.add_clause([-var_map[(u, iu)],  var_map[(v, jv)]])
                            solver.add_clause([-var_map[(v, jv)],  var_map[(u, iu)]])
                
            elif '>' in parts:
                # (5)
                for iu in vals_u:
                    if (iu - distance  <= vals_v[0] and iu + distance > vals_v[-1]):
                        solver.add_clause([-var_map[(u, iu)]]) #(5)
                    elif (iu - distance <= vals_v[0]):
                        for jv in vals_v:
                            if jv - iu > distance:
                               solver.add_clause([-var_map[(u, iu)], order_var_map[(v, jv)]]) #(6)
                               break
                    elif iu + distance > vals_v[-1]:
                        T = iu - distance 
                        # tìm nhãn gần nhất >= T
                        for t in vals_v:
                            if t >= T:
                                solver.add_clause([-var_map[(u, iu)], -order_var_map[(v, t)]]) #(7)
                                break
                    else : # (8)
                        limit_low  = iu - distance 
                        limit_high = iu + distance 

                        clause = [-var_map[(u, iu)]]
                        for t in vals_v:
                            if t >= limit_low:
                                clause.append(-order_var_map[(v, t)])
                                break
                        for t in vals_v:
                            if t >= limit_high:
                                clause.append(order_var_map[(v, t)])
                                break
                        if len(clause) > 1:
                            solver.add_clause(clause)   

                for jv in vals_v:
                    if (jv - distance  <= vals_u[0] and jv + distance > vals_u[-1]):
                        solver.add_clause([-var_map[(v, jv)]]) #(5)
                    elif (jv - distance <= vals_u[0]):
                        for iu in vals_u:
                            if jv - iu > distance:
                               solver.add_clause([-var_map[(v, jv)], order_var_map[(u, iu)]]) #(6)
                               break
                    elif jv + distance > vals_u[-1]:
                        T = jv - distance 
                        # tìm nhãn gần nhất >= T
                        for t in vals_u:
                            if t >= T:
                                solver.add_clause([-var_map[(v, jv)], -order_var_map[(u, t)]]) #(7)
                                break
                    else : # (8)
                        limit_low  = jv - distance 
                        limit_high = jv + distance 
                        clause = [-var_map[(v, jv)]]
                        for t in vals_u:
                            if t >= limit_low:
                                clause.append(-order_var_map[(u, t)])
                                break
                        for t in vals_u:
                            if t >= limit_high:
                                clause.append(order_var_map[(u, t)])
                                break
                        if len(clause) > 1:
                            solver.add_clause(clause)  

    
    
                            
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
    """
    Encode: sum(label_vars) <= UB using Sequential Counter
    Return:
        S: rhs counter variables (for assumptions)
    """

    label_vars = list(label_var_map.values())

    enc = CardEnc.atmost(
        lits=label_vars,
        bound=UB,
        encoding=EncType.seqcounter,
        top_id=solver.nof_vars()
    )

    for c in enc.clauses:
        solver.add_clause(c)

    # S[i] <=> sum(label_vars) <= i+1
    return enc.rhs

def add_limit_label_constraints(solver, lits, K):

    if isinstance(lits, dict):
        lits = list(lits.values())
    
    n = len(lits)
    top = solver.nof_vars()

    # s[i][j] : i in [0..n-1], j in [0..K-1]
    s = [[0] * K for _ in range(n)]

    # tạo biến phụ
    for i in range(n):
        for j in range(K):
            top += 1
            s[i][j] = top

    # (1) ¬x_i ∨ s[i][0]
    for i in range(n):
        solver.add_clause([-lits[i], s[i][0]])

    # (2) ¬s[i-1][j] ∨ s[i][j]
    for i in range(1, n):
        for j in range(K):
            solver.add_clause([-s[i-1][j], s[i][j]])

    # (3) ¬x_i ∨ ¬s[i-1][j-1] ∨ s[i][j]
    for i in range(1, n):
        for j in range(1, K):
            solver.add_clause([-lits[i], -s[i-1][j-1], s[i][j]])

    # (4) ¬x_i ∨ ¬s[i-1][K-1]
    for i in range(1, n):
        solver.add_clause([-lits[i], -s[i-1][K-1]])

    # rhs[j-1] <=> sum(lits) <= j
    rhs = [s[n-1][j] for j in range(K)]

    return rhs



def solve_and_print(solver, var_map, x_var, ub):
    if x_var != None and ub != None :
        solver.add_clause([-x_var[ub]])
    if solver.solve():
        model = solver.get_model()
        assignment = {}
        for (i, v), varnum in var_map.items():
            if model[varnum-1] > 0:
                assignment[i] = v
        print("Solution:")
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
    delete_invalid_labels(var, files["ctr"])
    last_var_num, var_map = create_var_map(var)

    print("Solve first problem:")
    solver = Solver(name='glucose4')
    # solver = Cadical195()
    build_constraints(solver, var, var_map, last_var_num, files["ctr"])

    assignment = solve_and_print(solver, var_map, None, None)
    if assignment is None:
        return
    if verify_solution_simple(assignment, var, files["ctr"]):
        print("Correct solution!")
        num_labels = len(set(assignment.values()))
        print("Number of lables used: ", num_labels)
    else:   
        print("Incorrect solution!")
        return
    end_time = time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    process = psutil.Process(os.getpid())
    print(f"Memory used: {process.memory_info().rss / 1024**2:.2f} MB")
    lable_var_map = create_label_var_map(domain[0], solver.nof_vars() + 1)
    build_label_constraints(solver, var_map, lable_var_map)
    rhs = add_limit_label_constraints(solver, lable_var_map,num_labels)

    

    while num_labels > 1:
        
        print("--------------------------------------------------")
        print(f"\nTrying with at most {num_labels - 1} labels...")
        assignment = solve_and_print(solver, var_map, rhs, num_labels - 1)
        if assignment is None:
            print("No more solutions found.")
            print("Optimal number of labels used: ", num_labels)
            print(f"Time taken: {time() - start_time:.2f} seconds")
            break
        if verify_solution_simple(assignment, var, files["ctr"]):
            print("Correct solution!")
            num_labels = len(set(assignment.values()))
            print("Number of lables used: ", num_labels)
            
            
        else:
            print("Incorrect solution!")
            break

        print(f"Time taken: {time() - start_time:.2f} seconds")
        process = psutil.Process(os.getpid())
        print(f"Memory used: {process.memory_info().rss / 1024**2:.2f} MB")

    solver.delete()

if __name__ == "__main__":
    main()