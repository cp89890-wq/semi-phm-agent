# EDA — cmp

파일 373개

- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-000.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-001.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-002.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-003.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-004.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-005.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-006.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-007.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-008.csv
- /home/claude/semi-phm-agent/data/raw/phm2016/2016 PHM DATA CHALLENGE CMP DATA SET/CMP-data/test/CMP-test-009.csv
- ...

### training 시계열 샘플 (CMP-training-000.csv)

- shape: (3663, 25)
- 결측 없음

|                              |           mean |            std |            min |             max |
|:-----------------------------|---------------:|---------------:|---------------:|----------------:|
| MACHINE_ID                   |    2           |    0           |    2           |     2           |
| MACHINE_DATA                 |    3.9754      |    1.4922      |    1           |     6           |
| TIMESTAMP                    |    4.8164e+08  | 6479.5         |    4.81634e+08 |     4.81657e+08 |
| WAFER_ID                     |   -2.65534e+09 |    1.93614e+09 |   -4.22416e+09 |     3.71447e+08 |
| CHAMBER                      |    3.9754      |    1.4922      |    1           |     6           |
| USAGE_OF_BACKING_FILM        | 9338.08        |   80.511       | 9253.33        |  9540           |
| USAGE_OF_DRESSER             |  536.058       |    4.7224      |  531.852       |   548.148       |
| USAGE_OF_POLISHING_TABLE     |  251.504       |   89.1954      |   65.9259      |   341.481       |
| USAGE_OF_DRESSER_TABLE       | 2667.6         |    3.1841      | 2664.75        |  2675.75        |
| PRESSURIZED_CHAMBER_PRESSURE |   52.7524      |   40.6989      |    0           |   150.476       |
| MAIN_OUTER_AIR_BAG_PRESSURE  |  170.328       |  143.021       |    0           |   498           |
| CENTER_AIR_BAG_PRESSURE      |   44.0277      |   36.7644      |    0           |   137.812       |
| RETAINER_RING_PRESSURE       | 1192.7         | 1384.78        |    0           | 10650.9         |
| RIPPLE_AIR_BAG_PRESSURE      |    6.4637      |    5.4182      |    0           |    20.0455      |
| USAGE_OF_MEMBRANE            |  110.728       |    0.9547      |  109.723       |   113.123       |
| USAGE_OF_PRESSURIZED_SHEET   | 2801.42        |   24.1535      | 2776           |  2862           |
| SLURRY_FLOW_LINE_A           |    4.2803      |    6.9519      |    0           |    32.9167      |
| SLURRY_FLOW_LINE_B           |    0.6902      |    0.3887      |    0           |     0.9091      |
| SLURRY_FLOW_LINE_C           |  258.851       |  221.988       |    0           |   593.6         |
| WAFER_ROTATION               |   11.0942      |   15.897       |    0           |    34.8837      |
| STAGE_ROTATION               |   49.4888      |   89.9391      |    0           |   263.026       |
| HEAD_ROTATION                |  160.007       |    6.8854      |  156.8         |   192           |
| DRESSING_WATER_STATUS        |    0.5425      |    0.4983      |    0           |     1           |
| EDGE_AIR_BAG_PRESSURE        |   30.9246      |   25.2022      |    0           |   106.364       |

### training removal rate (정답)

- shape: (1981, 3)
- 결측 없음

|                  |         mean |           std |          min |            max |
|:-----------------|-------------:|--------------:|-------------:|---------------:|
| WAFER_ID         |  8.92726e+08 |   2.60742e+09 | -4.23016e+09 |    4.22977e+09 |
| AVG_REMOVAL_RATE | 98.6316      | 187.429       | 53.4266      | 4326.15        |
