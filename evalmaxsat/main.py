import os
import sys
import time
import psutil
from pysat.formula import WCNF

from pysat.card import CardEnc, EncType

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
    return var

def delete_invalid_labels(var, ctr_file):
    constraint = {}
    with open(ctr_file) as f:
        for line in f:
            if line.strip() == '\x00':
                continue
            parts = line.strip().split()
            if not parts:
                continue
            u, v = int(parts[0]), int(parts[1])
            distance = int(parts[4])
            constraint[(u, v)] = (parts[3], distance)
            
    while True:
        changed = False
        for (u, v), (op, distance) in constraint.items():
            if op == '=':
                new_var_u = [label for label in var[u] if any(abs(label - label_v) == distance for label_v in var[v])]
                new_var_v = [label for label in var[v] if any(abs(label - label_u) == distance for label_u in new_var_u)]
            elif op == '>':
                new_var_u = [label for label in var[u] if any(abs(label - label_v) > distance for label_v in var[v])]
                new_var_v = [label for label in var[v] if any(abs(label - label_u) > distance for label_u in new_var_u)]
            else:
                continue

            if len(new_var_u) != len(var[u]) or len(new_var_v) != len(var[v]):
                changed = True
                var[u] = new_var_u
                var[v] = new_var_v
                
        for i, vals in var.items():
            if len(vals) == 0:
                print(f"Warning: variable {i} has no valid labels after preprocessing.")
                return False
        if not changed:
            break
    return True

def create_var_map(var):
    var_map = {}
    counter = 1
    for i, vals in var.items():
        for v in vals:
            var_map[(i, v)] = counter
            counter += 1
    return counter, var_map

def create_order_var_map(var, var_map, last_var_num, wcnf, stats=None):
    counter = last_var_num + 1
    order_var_map = {}

    for u, labels in var.items():
        for i in labels:
            order_var_map[(u, i)] = counter
            counter += 1

    if stats is not None:
        stats["order_vars"] = len(order_var_map)

    # Monotonicity constraints (Hard clauses cho POSE)
    for u, labels in var.items():
        if len(labels) <= 0:
            print("Warning: variable", u, "has no valid labels.")
            return
            
        last_i = labels[-1]
        wcnf.append([-var_map[(u, last_i)], order_var_map[(u, last_i)]])
        wcnf.append([-order_var_map[(u, last_i)], var_map[(u, last_i)]])
        if stats is not None:
            stats["order_clauses"] += 2
        
        for idx in range(1, len(labels)):
            wcnf.append([-order_var_map[(u, labels[idx])], order_var_map[(u, labels[idx - 1])]])
            if stats is not None:
                stats["order_clauses"] += 1
        wcnf.append([order_var_map[(u, labels[0])]])
        if stats is not None:
            stats["order_clauses"] += 1
        
        for idx in range(len(labels)-1):
            wcnf.append([-var_map[(u, labels[idx])], order_var_map[(u, labels[idx])]])
            wcnf.append([-var_map[(u, labels[idx])], -order_var_map[(u, labels[idx + 1])]])  
            wcnf.append([-order_var_map[(u, labels[idx])], order_var_map[(u, labels[idx + 1])], var_map[(u, labels[idx])]])
            if stats is not None:
                stats["order_clauses"] += 3

    return counter - 1, order_var_map

def build_constraints_POSE(wcnf, var, var_map, last_var_num, ctr_file, stats=None):
    # Phương pháp 1: Product/Position/Order-based Encoding
    counter, order_var_map = create_order_var_map(var, var_map, last_var_num, wcnf, stats)

    with open(ctr_file) as f:
        for line in f:
            if line.strip() == '\x00':
                continue
            parts = line.strip().split()
            if not parts:
                continue

            u, v = int(parts[0]), int(parts[1])
            vals_u = var.get(u, [])
            vals_v = var.get(v, [])
            distance = int(parts[4])
            
            if '=' in parts:
                for iu in vals_u:
                    wcnf.append([-var_map[(u, iu)]] + [var_map[(v, jv)] for jv in vals_v if abs(iu - jv) == distance])
                    if stats is not None:
                        stats["distance_clauses"] += 1
            elif '>' in parts:
                for iu in vals_u:
                    if (iu - distance <= vals_v[0]):
                        for jv in vals_v:
                            if jv - iu > distance:
                               wcnf.append([-var_map[(u, iu)], order_var_map[(v, jv)]])
                               if stats is not None:
                                   stats["distance_clauses"] += 1
                               break
                    elif iu + distance >= vals_v[-1]:
                        T = iu - distance 
                        for t in vals_v:
                            if t >= T:
                                wcnf.append([-var_map[(u, iu)], -order_var_map[(v, t)]])
                                if stats is not None:
                                    stats["distance_clauses"] += 1
                                break
                    else: 
                        limit_low  = iu - distance 
                        limit_high = iu + distance 
                        clause = [-var_map[(u, iu)]]
                        for t in vals_v:
                            if t >= limit_low:
                                clause.append(-order_var_map[(v, t)])
                                break
                        for t in vals_v:
                            if t > limit_high:
                                clause.append(order_var_map[(v, t)])
                                break
                        if len(clause) > 1:
                            wcnf.append(clause)   
                            if stats is not None:
                                stats["distance_clauses"] += 1
    return counter

def build_constraints_DSE(wcnf, var, var_map, ctr_file, type_card, stats=None):
    # Phương pháp 2: Direct Encoding (Sử dụng CardEnc cho ràng buộc Exactly-One)
    top_id = max(var_map.values())

    # Ràng buộc Đúng-Một-Nhãn (Exactly One) cho mỗi biến
    for i, vals in var.items():
        lits = [var_map[(i, v)] for v in vals]
        enc = CardEnc.equals(lits, bound=1, top_id=top_id, encoding=type_card)
        for clause in enc.clauses:
            wcnf.append(clause)
        if stats is not None:
            stats["card_clauses"] += len(enc.clauses)
        top_id = enc.nv

    if stats is not None:
        stats["card_aux_vars"] = top_id - max(var_map.values())

    # Ràng buộc khoảng cách (Distance constraints)
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
            
            if '>' in parts:
                distance = int(parts[4])
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) <= distance:
                            wcnf.append([-var_map[(i, vi)], -var_map[(j, vj)]])
                            if stats is not None:
                                stats["distance_clauses"] += 1
                            
            elif '=' in parts:
                target = int(parts[4])
                for vi in vals_i:
                    wcnf.append([-var_map[(i, vi)]] + [var_map[(j, vj)] for vj in vals_j if abs(vi - vj) == target])
                    if stats is not None:
                        stats["distance_clauses"] += 1
    
    return top_id

def create_label_var_map(labels, start_index):
    label_var_map = {}
    current = start_index
    for lb in labels:
        label_var_map[lb] = current
        current += 1
    return label_var_map

def build_maxsat_label_constraints(wcnf, var_map, label_var_map, stats=None):
    for (i, v), varnum in var_map.items():
        lb_varnum = label_var_map[v]
        wcnf.append([-varnum, lb_varnum])
        if stats is not None:
            stats["label_link_clauses"] += 1

    for v, lb_varnum in label_var_map.items():
        wcnf.append([-lb_varnum], weight=1)
    if stats is not None:
        stats["label_vars"] = len(label_var_map)
        stats["soft_clauses"] = len(label_var_map)

def main():
    start_time = time.perf_counter()
    
    helpers = "Usage: python3 main.py <dataset_folder> <encoding_method> [<card_encoding>]\n" \
              "  encoding_method: 'POSE' or 'DSE'\n" \
              "  card_encoding (only for DSE): integer corresponding to Cardinality encoding (default: 1 - seqcounter)\n"
              
    if len(sys.argv) < 3:
        print(helpers)
        return

    encoding_method = sys.argv[2].upper()
    if encoding_method not in ['POSE', 'DSE']:
        print(f"Lỗi: Phương pháp mã hóa không hợp lệ.\n{helpers}")
        return

    # Cấu hình loại mã hóa cardinality cho hàm DSE nếu người dùng truyền vào
    type_card = int(sys.argv[3] if len(sys.argv) >= 4 else 1)  # Mặc định là 1 (seqcounter)
    if encoding_method == 'DSE' and len(sys.argv) >= 4:
        try:
            type_card = int(sys.argv[3])
        except ValueError:
            print("Lỗi: card_encoding phải là một số nguyên.")
            return

    dataset_folder = os.path.join("dataset", sys.argv[1])

    try:
        files = get_file_names(dataset_folder)
    except ValueError as e:
        print(e)
        return

    domain = read_domain(files["domain"])
    var = read_var(files["var"], domain)
    if not delete_invalid_labels(var, files["ctr"]):
        print("No solution found in the preprocessing step!")
        return
        
    last_var_num, var_map = create_var_map(var)
    wcnf = WCNF()

    stats = {
    # variables
    "decision_vars": 0,
    "order_vars": 0,
    "card_aux_vars": 0,
    "label_vars": 0,

    # clauses
    "order_clauses": 0,
    "card_clauses": 0,
    "distance_clauses": 0,
    "label_link_clauses": 0,
    "soft_clauses": 0,
}
    stats["decision_vars"] = len(var_map)
    # Nhánh kiểm soát phương pháp Encoding qua tham số đầu vào
    if encoding_method == 'POSE':
        print("---  POSE  ---")
        top_var_num = build_constraints_POSE(wcnf, var, var_map, last_var_num, files["ctr"], stats)
    else:
        print(f"---  DSE  [Cardinality Encoding: {type_card}] ---")
        top_var_num = build_constraints_DSE(wcnf, var, var_map, files["ctr"], type_card, stats)

    # Khởi tạo các biến quản lý nhãn dựa trên top_var_num nhận về từ hàm tương ứng
    label_var_map = create_label_var_map(domain[0], top_var_num + 1)
    
    # Xây dựng các ràng buộc mềm/cứng để tối ưu hóa số nhãn
    build_maxsat_label_constraints(wcnf, var_map, label_var_map, stats)

    stats["total_vars"] = wcnf.nv
    stats["hard_clauses"] = len(wcnf.hard)
    stats["total_clauses"] = len(wcnf.hard) + len(wcnf.soft)

    # output file
    if encoding_method == "POSE":
        outfile = (
            sys.argv[4]
            if len(sys.argv) >= 5
            else f"{sys.argv[1]}_POSE.wcnf"
        )
    else:
        outfile = (
            sys.argv[4]
            if len(sys.argv) >= 5
            else f"{sys.argv[1]}_DSE_{type_card}.wcnf"
        )

    wcnf.to_file(outfile)
    with open(outfile, "r") as f:
        content = f.read()

    comments = [
        f"c Dataset: {sys.argv[1]}",
        f"c Encoding: {encoding_method}",
        f"c DecisionVars: {stats['decision_vars']}",
        f"c OrderVars: {stats['order_vars']}",
        f"c CardinalityAuxVars: {stats['card_aux_vars']}",
        f"c LabelVars: {stats['label_vars']}",
        f"c TotalVars: {stats['total_vars']}",
        f"c OrderClauses: {stats['order_clauses']}",
        f"c CardinalityClauses: {stats['card_clauses']}",
        f"c DistanceClauses: {stats['distance_clauses']}",
        f"c LabelLinkClauses: {stats['label_link_clauses']}",
        f"c SoftClauses: {stats['soft_clauses']}",
        f"c HardClauses: {stats['hard_clauses']}",
        f"c TotalClauses: {stats['total_clauses']}",
        ""
    ]

    with open(outfile, "w") as f:
        f.write("\n".join(comments))
        f.write(content)
    print("\n--------------------------------------------------")
    print("WCNF generated successfully")
    print(f"Output file : {outfile}")
    print(f"Variables   : {wcnf.nv}")
    print(f"Hard clauses: {len(wcnf.hard)}")
    print(f"Soft clauses: {len(wcnf.soft)}")
    print(f"Total clauses: {len(wcnf.hard) + len(wcnf.soft)}")
if __name__ == "__main__":
    main()