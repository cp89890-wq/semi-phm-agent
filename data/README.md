# 데이터

원본은 git에 올리지 않는다. 아래 위치에 직접 풀어둔다.

```
data/raw/phm2016/   CMP-training-*.csv, CMP-training-removalrate.csv, CMP-test-*.csv (+ test 정답)
data/raw/phm2018/   train/, test/ (장비별 csv), train/train_faults/, train/train_tff/
```

## 출처

| 데이터 | 1차 | 2차(보존본) |
|---|---|---|
| PHM 2016 CMP | Kaggle `markshizhe/cmp-data-set` (test 정답 포함) | Internet Archive의 원본 zip |
| PHM 2018 이온밀 | PHM Society 공식 Google Drive | NASA DashLink 미러 |

링크는 `scripts/download_data.py` 참고. 받은 날짜와 파일 해시를 아래에 기록한다.

## 수령 기록

| 날짜 | 데이터 | 파일명 | SHA256 (앞 12자리) |
|---|---|---|---|
| 2026-11-05 | PHM 2016 CMP 본체 (Internet Archive 보존본, 2016-05-17 판) | 2016_PHM_DATA_CHALLENGE_CMP_DATA_SET.zip (9.4MB) | 3d504c5051c9 |
| 2026-11-05 | PHM 2016 CMP test 정답 (Kaggle markshizhe/cmp-data-set) | archive.zip → CMP-test-removalrate_V3.csv | d575f62f21db |
