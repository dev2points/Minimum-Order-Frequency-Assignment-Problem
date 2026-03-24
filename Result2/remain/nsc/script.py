import os
import csv
import re

def parse_log(file_path):
    problem = None
    value = '-'
    time_val = None
    status = None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # 🔥 LẤY ĐÚNG dòng cuối cùng chứa "Total time" hoặc "Time taken"
    for line in reversed(lines):
        if 'Total time' in line or 'Time taken' in line:
            # match số sau dấu :
            match_time = re.search(r':\s*([\d\.]+)', line)
            if match_time:
                time_val = float(match_time.group(1))
                break

    for line in lines:
        # Tên problem
        if '[runlim] argv[3]:' in line:
            problem = line.split()[-1]

        # Status
        if '[runlim] status:' in line:
            if 'out of time' in line:
                status = 'TO'
            elif 'out of memory' in line:
                status = 'MO'

        # Value
        if 'Number of lables used:' in line:
            match = re.search(r'Number of lables used:\s*(\d+)', line)
            if match:
                value = int(match.group(1))

    # 🔥 Xử lý status
    if status not in ['TO', 'MO']:
        if value is not None:
            status = 'OPT'
        else:
            status = 'INF'

    # 🔥 TO → time = 600
    if status == 'TO':
        time_val = 600.0

    return problem, value, time_val, status


# 🔥 sort: scen → graph → TUD + natural number
def custom_sort(name):
    name_lower = name.lower()

    if name_lower.startswith('scen'):
        group = 0
    elif name_lower.startswith('graph'):
        group = 1
    elif name_lower.startswith('tud'):
        group = 2
    else:
        group = 3

    match = re.search(r'(\d+)', name_lower)
    number = int(match.group(1)) if match else float('inf')

    return (group, number, name_lower)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(current_dir, 'result.csv')

    log_files = [f for f in os.listdir(current_dir) if f.endswith('.log')]

    results = []

    for file_name in log_files:
        full_path = os.path.join(current_dir, file_name)

        problem, value, time_val, status = parse_log(full_path)

        if problem is None:
            problem = file_name

        results.append((problem, value, time_val, status))

    # 🔥 sort chuẩn
    results.sort(key=lambda x: custom_sort(x[0]))

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Problem', 'Value', 'Time', 'Status'])

        for row in results:
            writer.writerow(row)

    print(f"Done! File saved at: {output_csv}")


if __name__ == "__main__":
    main()