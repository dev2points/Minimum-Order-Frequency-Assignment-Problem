# Extractor and Workbook Pending Notes

File nay ghi rieng tinh trang cong viec dang do quanh:

- extractor log -> CSV tong
- validate ket qua cu
- generate workbook moi

No khong thay the code; no la checklist thao tac va note de tranh lam sai logic.

## 1. Muc tieu

Can co mot pipeline sach de:

1. extract `status`, `report_value`, `report_time_s` cho tat ca cac phuong phap can dua vao bang;
2. validate cac ket qua cu voi log/workbook cu;
3. generate workbook moi va 2 file CSV tu mot nguon du lieu nhat quan.

## 2. Nguyen tac parse da chot

- Uu tien `runlim` truoc moi tin hieu in boi Python.
- Neu `[runlim] status: out of time`:
  - `status = timeout`
  - `report_value` de trong
  - `report_time_s = 600`
- Neu process chay xong va Python kip in ket qua:
  - moi duoc lay `report_value`.
- Khong duoc lay bound dang thu lam ket qua:
  - khong dung `Trying with at most K labels...` de dien vao cot value.
- `Total time` va `Time taken` khong giong nhau:
  - `Total time` la moc Python end-to-end neu log co in.
  - `Time taken` co the chi la incumbent callback hoac nhanh thoat som.

## 3. Tinh trang hien tai theo tung nhom

### CPSAT / CPSAT_CP

- Da review code goc: `Status: ...` duoc in tu `solver.StatusName(status)`.
- Da sua `parse_cpsat_log()` de:
  - lay `report_value` tu `Number of labels used` hoac `Objective value`
  - nhung chi khi khong timeout/oom va co status ket thuc hop le
- Khong can sua them neu chi xet logic timeout-vs-status.

### Cardinality

- Da review code goc `SAT/pairwise/pairwise.py` va `pairwise_no_preprocessing.py`.
- Parse hien tai:
  - da phan biet timeout bang `runlim`
  - da dung `Total time` / `Time taken` theo kieu tương doi hop ly
  - chua fill `report_value`
- Viec can lam:
  - them `report_value` cho `parse_cardinality_log()`
  - chi lay tu ket luan cuoi hop le
  - khong lay tu cac nghiem trung gian
  - khong lay tu `Trying with at most K labels...`

### Legacy

- Da co script validate so cu voi workbook cu.
- Legacy parse dung duoc de trace lai ket qua cu.
- Co 2 case lech da phat hien truoc day do cach uu tien `Total time` / `Time taken`.
- Khong nen sua tiep legacy neu chua can, vi muc tieu truoc mat la fill current methods cho workbook moi.

## 4. Viec phai lam not truoc khi generate workbook

### A. Hoan thien extractor

- [x] CPSAT: fill `report_value`
- [ ] Cardinality: fill `report_value`
- [ ] Rerun extractor de sinh CSV tong moi
- [ ] Kiem tra tay it nhat 1 case optimal, 1 timeout, 1 infeasible som

### B. Chot schema CSV tong

CSV tong can co it nhat cac cot sau:

- `source_family`
- `method`
- `variant`
- `preprocessing`
- `dataset`
- `status`
- `report_value`
- `report_time_s`
- `report_time_rule`
- `python_e2e_time_s`
- `time_taken_s`
- `total_time_s`
- `time_taken_role`
- `timeout_limit_s`
- `log_path`

### C. Validate

- [ ] Doi chieu current CSV tong voi mot vai log mau
- [ ] Doi chieu legacy CSV/workbook cu voi log mau
- [ ] Chot quy uoc output:
  - timeout -> value trong, time = 600
  - infeasible -> value trong, time la moc Python ket thuc hop le
  - optimal/feasible -> co value, co time

### D. Generate workbook moi

- [ ] Chi bat dau khi extractor da fill du current methods
- [ ] Generate 2 CSV:
  - preprocessing
  - no_preprocessing
- [ ] Sau do moi generate workbook tong hop

## 5. Cac file code lien quan

- `SourceCode/stats_csv/tools/extract_python_total_times.py`
- `SourceCode/stats_csv/tools/validate_legacy_results_against_workbook.py`
- `SourceCode/stats_csv/tools/generate_comparison_workbook.py`

## 6. Cac file log mau da dung de review

- `SourceCode/CPSAT/results/preprocessing/graph02.log`
- `SourceCode/CPSAT/results/no_preprocessing/graph01.log`
- `SourceCode/SAT/pairwise/results/preprocessing/matched_cardnetwrk/graph01.log`
- `SourceCode/SAT/pairwise/results/preprocessing/matched_cardnetwrk/scen06.log`

## 7. Rule thao tac

- Moi sua code extractor phai lam tung ham mot.
- Truoc khi sua, noi ro se sua ham nao va logic nao.
- Sau moi sua, phai bao lai chinh xac da doi cho nao.
- Chua generate workbook chot khi extractor chua fill du.

## 8. Luu y bo sung de xem lai sau

- Khong chi current methods, ma ca nhieu phuong phap cu cung co the gap hien tuong:
  - da co incumbent hoac loi giai tot nhat tam thoi o bound truoc;
  - sau do `runlim` cat process khi dang thu bound tiep theo;
  - Python khong kip in ket luan cuoi.
- Vi vay, voi cac phuong phap iterative / bound-tightening:
  - log co the chua thong tin ve loi giai da tim thay truoc timeout;
  - nhung neu khong co ket luan cuoi hop le thi bang chinh van phai xem la `timeout`.
- Can xem lai sau khi xong extractor:
  - co can mot cot rieng cho "best solution seen before timeout" hay khong;
  - hay chi giu mot schema don gian: `TO` va khong ghi `report_value`.
- Nhom de can than nhat:
  - `POSE/DSE + INC/INCSC`
  - `cardinality`
  - `CPSAT` callback-based logs
