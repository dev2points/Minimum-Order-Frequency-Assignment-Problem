# Ghi chu ve cac cot thoi gian trong cac file `python_total_times_*.csv`

File nay dung de giai thich y nghia cac cot thoi gian da extract tu log cua:

- `CPSAT`
- `CPSAT_CP`
- nhom `cardinality` trong `SAT/pairwise/results/matched_*`

## 1. Cac cot hien co

Trong file CSV hien tai co hai cot:

- `time_taken_s`
- `total_time_s`

## 2. Y nghia cua `total_time_s`

`total_time_s` la thoi gian Python do tu luc bat dau chuong trinh den luc chuong trinh in dong `Total time`.

Day la cot nen uu tien neu muon thong nhat voi cach do thoi gian cu trong bao cao.

### Doi voi `CPSAT` va `CPSAT_CP`

Dong nay co dang:

- `Total time: 0.43s`

### Doi voi `cardinality`

Dong nay co dang:

- `Total time: 56.14 seconds`

## 3. Y nghia cua `time_taken_s`

`time_taken_s` khong phai luc nao cung la thoi gian chay xong.

No chi la gia tri in ra tu dong `Time taken`.

### Doi voi `CPSAT` va `CPSAT_CP`

`Time taken` duoc in trong callback moi khi solver tim duoc mot incumbent moi.

Vi vay:

- neu log bi `runlim` kill do timeout, log van co the co `Time taken`
- nhung gia tri nay chi la thoi diem tim duoc incumbent cuoi cung
- no khong phai tong thoi gian chay cua run

Do do, voi `CPSAT` va `CPSAT_CP`:

- khong duoc dung `time_taken_s` de thay cho `total_time_s`
- neu `status = timeout`, phai xem `time_taken_s` la moc incumbent, khong phai run time cuoi

### Doi voi `cardinality`

Trong `pairwise.py`, `Time taken` xuat hien chu yeu o cac nhanh thoat som, vi du:

- preprocessing lam rong mien
- bai toan feasibility dau tien UNSAT
- lan kiem tra tiep theo UNSAT va chuong trinh `return`

Trong khi do, `Total time` duoc in o cac moc ma chuong trinh da di het mot pha lon hon hoac ket thuc binh thuong.

Vi vay:

- `time_taken_s` cua `cardinality` co the phan anh mot nhanh that bai som
- `total_time_s` moi la cot can uu tien neu muon lay "thoi gian Python chay tu dau den cuoi"

## 4. Cach dung de viet bao cao

Neu muc tieu la thong nhat voi "thoi gian Python do tu luc bat dau den luc chay xong", thi:

- uu tien dung `total_time_s`
- khong dung `time_taken_s` de thay the cho `total_time_s`

## 5. Cach xu ly timeout

Neu mot run bi timeout boi `runlim`:

- co the log khong co `Total time` cuoi cung do Python chua kip in
- `time_taken_s` neu co chi la incumbent time

Do do:

- `status = timeout` thi khong nen dung `time_taken_s` lam tong thoi gian
- neu can thoi gian gioi han thuc te cua timeout, phai doc tu `runlim real`

## 6. Ket luan ngan

- `total_time_s`: gan nhat voi "Python end-to-end time"
- `time_taken_s`: cot tham khao, khong phai luc nao cung la tong thoi gian
- doi voi `CPSAT`/`CPSAT_CP`, timeout rat de gay nham neu nhin vao `time_taken_s`
