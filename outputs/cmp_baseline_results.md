# CMP 베이스라인 결과

웨이퍼 1977개, 이상치 4건 제외, LightGBM, 시드 42

| split   |   n_train |   n_val |   rmse_all |   rmse_ch123 |   n_ch123 |   rmse_ch456 |   n_ch456 |   rmse_naive_chamber_mean |
|:--------|----------:|--------:|-----------:|-------------:|----------:|-------------:|----------:|--------------------------:|
| time    |      1581 |     396 |      6.111 |        5.636 |        69 |        6.206 |       327 |                     7.829 |
| random  |      1581 |     396 |      3.488 |        3.25  |        74 |        3.541 |       322 |                     8.077 |

## 특징 중요도 상위 15 (시간순 분할 모델)

|                                |   0 |
|:-------------------------------|----:|
| USAGE_OF_DRESSER_TABLE__mean   | 544 |
| USAGE_OF_DRESSER__mean         | 520 |
| USAGE_OF_BACKING_FILM__mean    | 513 |
| USAGE_OF_POLISHING_TABLE__mean | 400 |
| duration                       | 334 |
| SLURRY_FLOW_LINE_A__mean       | 242 |
| SLURRY_FLOW_LINE_C__std        | 240 |
| DRESSING_WATER_STATUS__frac    | 240 |
| SLURRY_FLOW_LINE_C__mean       | 210 |
| HEAD_ROTATION__std             | 208 |
| RETAINER_RING_PRESSURE__max    | 205 |
| STAGE_ROTATION__mean           | 201 |
| CENTER_AIR_BAG_PRESSURE__mean  | 198 |
| HEAD_ROTATION__mean            | 191 |
| STAGE_ROTATION__frac           | 186 |