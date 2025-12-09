from multiprocessing import process
import os
import sys
import psutil
from time import time
from gurobipy import Model, GRB


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
    return var


def build_gurobi_model(var, ctr_file):
    model = Model("MOFAP")
    model.Params.OutputFlag = 0


    # binary variable 
    x = {}
    for i, vals in var.items():
        for v in vals:
            x[(i, v)] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{v}")

    # label variable 
    label_set = sorted({v for vals in var.values() for v in vals})
    y = {}
    for lb in label_set:
        y[lb] = model.addVar(vtype=GRB.BINARY, name=f"y_{lb}")

    model.update()

    #exactly one
    for i, vals in var.items():
        model.addConstr(sum(x[(i, v)] for v in vals) == 1)

    # Link binary variables to label usage
    for (i, v), xv in x.items():
        model.addConstr(xv <= y[v])

    # distance constraints
    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            i, j = int(parts[0]), int(parts[1])
            vals_i = var[i]
            vals_j = var[j]

            if '>' in parts:
                distance = int(parts[4])
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) <= distance:
                            model.addConstr(x[(i, vi)] + x[(j, vj)] <= 1)

            elif '=' in parts:
                target = int(parts[4])
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) == target:
                            model.addConstr(x[(i, vi)] == x[(j, vj)])

    # Minimize number of labels used
    #model.setObjective(sum(y[v] for v in label_set), GRB.MINIMIZE)

    return model, x, y


def extract_solution(model, x):
    solution = {}
    for (i, v), var in x.items():
        if var.X > 0.5:
            solution[i] = v
    return solution
def verify_solution(solution, var, ctr_file):

    # Check each variable has 1 value and in domain
    for i, allowed_vals in var.items():
        if i not in solution:
            print(f"Variable {i} missing in solution")
            return False

        if solution[i] not in allowed_vals:
            print(f"Variable {i} has value {solution[i]} not in domain {allowed_vals}")
            return False

    # Check distance constraints
    with open(ctr_file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            i, j = int(parts[0]), int(parts[1])
            vi = solution[i]
            vj = solution[j]

            if '>' in parts:
                distance = int(parts[4])
                if abs(vi - vj) <= distance:
                    print(f"Constraint violated: |{vi}-{vj}| <= {distance}")
                    return False

            elif '=' in parts:
                target = int(parts[4])
                if abs(vi - vj) != target:
                    print(f"Constraint violated: |{vi}-{vj}| != {target}")
                    return False

    return True



def main():
    start_time = time()
    Time = start_time

    if len(sys.argv) < 2:
        print("Use: python main.py <dataset_folder>")
        return

    dataset_folder = os.path.join("dataset", sys.argv[1])

    files = get_file_names(dataset_folder)

    domain = read_domain(files["domain"])
    var = read_var(files["var"], domain)

    print("Building Gurobi model...")
    model, x, y = build_gurobi_model(var, files["ctr"])
    print(f"Build time used: {time() - start_time:.2f} sec")
    start_time = time()

    print("Solving...")
    model.optimize()

    if model.status != GRB.OPTIMAL:
        print("No solution found.")
        print(f"Solve time used: {time() - start_time:.2f} sec")
        return

    solution = extract_solution(model, x)
    used_labels = len(set(solution.values()))
    print(f"Solve time used: {time() - start_time:.2f} sec")
    print("Solution")
    print("{" + ", ".join(f"{solution[i]}" for i in sorted(solution)) + "}")
    print("Labels used:", used_labels)
    if verify_solution(solution, var, files["ctr"]):
        print("Solution is CORRECT!")
    else:
        print("Solution is WRONG!")
    
    print(f"Total time used: {time() - Time:.2f} sec")
    process = psutil.Process(os.getpid())
    print(f"Memory used: {process.memory_info().rss / 1024**2:.2f} MB")
    print("========================\n")
    
    while True:
        start_time = time()
        Time = start_time
        # Sao chép model
        print(f"\nTrying to find UB = {used_labels - 1}...")
        model2 = model.copy()

        # Lấy lại biến x, y từ model2
        x2 = {}
        y2 = {}

        for (i, v) in x:
            x2[(i, v)] = model2.getVarByName(f"x_{i}_{v}")

        for v in y:
            y2[v] = model2.getVarByName(f"y_{v}")

        # Thêm ràng buộc mới vào model2  
        model2.addConstr(sum(y2[v] for v in y2) <= used_labels - 1)
        print(f"Build time used: {time() - start_time:.2f} sec")

        # Giải
        model2.optimize()

        print(f"Solve time used: {time() - start_time:.2f} sec")
        if model2.status != GRB.OPTIMAL:
            print("No better solution found.")
            break

        solution = extract_solution(model2, x2)
        used_labels = len(set(solution.values()))

        print("Solution: ")
        print("{" + ", ".join(f"{solution[i]}" for i in sorted(solution)) + "}")
        print("Labels used:", used_labels)

        if verify_solution(solution, var, files["ctr"]):
            print("Solution is CORRECT!")
            # Cập nhật model hiện tại
            model = model2
            x = x2
            y = y2
        else:
            print("Solution is WRONG!")
            break
        
        print(f"Total time used: {time() - Time:.2f} sec")
        process = psutil.Process(os.getpid())
        print(f"Memory used: {process.memory_info().rss / 1024**2:.2f} MB")
        print("========================\n")


if __name__ == "__main__":
    main()
