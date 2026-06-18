# Run Experiments Handoff

Tai lieu nay de dong doi co the tiep tuc chay thuc nghiem ma khong phai doan lai thu tu uu tien.

## 1. Uu tien hien tai

Uu tien hien tai la:

1. chay not thuc nghiem `MaxSAT`
2. chay not thuc nghiem `evalmaxsat`
3. sau do moi quay lai extract lai `clause/var` cho `SAT` thuong

Ly do:

- `SAT` thuong da co script extract lai cong thuc
- `MaxSAT` va `evalmaxsat` dang la phan can them ket qua truoc
- extractor cua `MaxSAT/evalmaxsat` co the de sau, khong can gap ngay

## 2. Nhung thu muc lien quan

- `SourceCode/MaxSAT`
- `SourceCode/evalmaxsat`
- `SourceCode/SAT/pairwise`
- `SourceCode/SAT/sequence`
- `SourceCode/stats_csv/tools`

## 3. Chay MaxSAT truoc

### 3.1. Cac baseline hien co

Trong `SourceCode/MaxSAT` hien co:

- `POSE.sh`
- `POSEno.sh`
- `DSE.sh`
- `DSEno.sh`
- `CARD_seqcounter.sh`
- `CARD_seqcounter_no.sh`
- `CARD_totalizer.sh`
- `CARD_totalizer_no.sh`
- `CARD_ladder.sh`
- `CARD_ladder_no.sh`
- `CARD_kmtotalizer.sh`
- `CARD_kmtotalizer_no.sh`

`auto.sh` chi la wrapper goi lan luot cac file tren.

### 3.2. Cach chay

Vao thu muc:

```bash
cd SourceCode/MaxSAT
```

Neu muon chay tung baseline rieng:

```bash
./POSE.sh
./POSEno.sh
./DSE.sh
./DSEno.sh
./CARD_seqcounter.sh
./CARD_seqcounter_no.sh
./CARD_totalizer.sh
./CARD_totalizer_no.sh
./CARD_ladder.sh
./CARD_ladder_no.sh
./CARD_kmtotalizer.sh
./CARD_kmtotalizer_no.sh
```

Neu muon chay ca loat:

```bash
./auto.sh
```

### 3.3. Ghi chu quan trong

- `DSE` va `CARD` la hai baseline khac nhau
- `DSE` khong duoc xem la `CARD`
- `CARD` la baseline dung encoding thu vien cho constraints

## 4. Chay evalmaxsat sau MaxSAT

### 4.1. Cac baseline hien co

Trong `SourceCode/evalmaxsat` hien co:

- `POSE.sh`
- `POSEno.sh`
- `DSE.sh`
- `DSEno.sh`
- `CARD_seqcounter.sh`
- `CARD_seqcounter_no.sh`
- `CARD_totalizer.sh`
- `CARD_totalizer_no.sh`
- `CARD_ladder.sh`
- `CARD_ladder_no.sh`
- `CARD_kmtotalizer.sh`
- `CARD_kmtotalizer_no.sh`

`auto.sh` chi la wrapper goi lan luot cac file tren.

### 4.2. Cach chay

```bash
cd SourceCode/evalmaxsat
```

Chay tung baseline:

```bash
./POSE.sh
./POSEno.sh
./DSE.sh
./DSEno.sh
./CARD_seqcounter.sh
./CARD_seqcounter_no.sh
./CARD_totalizer.sh
./CARD_totalizer_no.sh
./CARD_ladder.sh
./CARD_ladder_no.sh
./CARD_kmtotalizer.sh
./CARD_kmtotalizer_no.sh
```

Hoac chay ca loat:

```bash
./auto.sh
```

### 4.3. Ghi chu quan trong

- `evalmaxsat` hien da tach `POSE`, `DSE`, `CARD`
- naming moi cua `CARD` la theo dang `CARD_<exact>_<amo>`
- extractor cho `evalmaxsat` chua uu tien sua ngay, co the de sau

## 5. Sau khi chay xong moi quay lai extract var/clause cho SAT thuong

### 5.1. SAT pairwise

Trong `SourceCode/SAT/pairwise` hien da co cac wrapper ro rang:

- `DSE_seqcounter_pre.sh`
- `DSE_seqcounter_no.sh`
- `DSE_totalizer_pre.sh`
- `DSE_totalizer_no.sh`
- `DSE_ladder_pre.sh`
- `DSE_ladder_no.sh`
- `DSE_kmtotalizer_pre.sh`
- `DSE_kmtotalizer_no.sh`
- `CARD_seqcounter_pre.sh`
- `CARD_seqcounter_no.sh`
- `CARD_totalizer_pre.sh`
- `CARD_totalizer_no.sh`
- `CARD_ladder_pre.sh`
- `CARD_ladder_no.sh`
- `CARD_kmtotalizer_pre.sh`
- `CARD_kmtotalizer_no.sh`

`auto.sh` trong thu muc nay goi lan luot cac script tren.

### 5.2. SAT sequence

Trong `SourceCode/SAT/sequence` hien da co:

- `INC.sh`
- `INCSC_NSC.sh`
- `INCSC_NSC_no.sh`
- `INCSC_TOT.sh`
- `INCSC_TOT_no.sh`

Can nho:

- `INC` va `INCSC` khac nhau
- `var/clause` cua `INC` va `INCSC` khong duoc gom chung nhu cung mot baseline

### 5.3. Script extract hien co

Cho SAT thuong, extractor hien co la:

- `SourceCode/SAT/pairwise/extract_pairwise_stats.py`
- `SourceCode/SAT/sequence/extract_sequence_stats.py`

Script Python tong hop cho SAT thuong:

- `SourceCode/stats_csv/tools/run_extract_classic_sat_stats.py`

Mac dinh script nay se sinh:

- `pairwise_stats_all.csv`
- `sequence_stats_all.csv`
- `classic_sat_stats_all.csv`

trong:

- `SourceCode/stats_csv/generated_comparison`

### 5.4. Lenh chay script extract tong cho SAT thuong

```powershell
C:\Users\ADMIN\AppData\Local\Programs\Python\Python312\python.exe D:\Research\FrequencyAssignment\SourceCode\stats_csv\tools\run_extract_classic_sat_stats.py
```

Neu muon tu chi dinh Python/output:

```powershell
python D:\Research\FrequencyAssignment\SourceCode\stats_csv\tools\run_extract_classic_sat_stats.py --python-exe C:\Users\ADMIN\AppData\Local\Programs\Python\Python312\python.exe --output-dir D:\Research\FrequencyAssignment\SourceCode\stats_csv\generated_comparison
```

## 6. Thu tu de xuat cho dong doi

Thu tu de xuat:

1. chay `SourceCode/MaxSAT`
2. chay `SourceCode/evalmaxsat`
3. kiem tra log va ket qua co du chua
4. sau cung moi chay `run_extract_classic_sat_stats.py` de lay `var/clause` cho SAT thuong

## 7. Nhung thu chua uu tien luc nay

Tam thoi chua uu tien:

- sua extractor moi cho `MaxSAT`
- sua extractor moi cho `evalmaxsat`
- don dep naming cu cua tat ca wrapper trong `MaxSAT/evalmaxsat`

Ly do la muc tieu truoc mat la co du ket qua chay.
