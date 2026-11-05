# EDA — ionmill

파일 65개

- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\test\01_M02_DC_test.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\test\02_M02_DC_test.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\test\03_M01_DC_test.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\test\04_M01_DC_test.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\test\06_M01_DC_test.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\train\01_M01_DC_train.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\train\01_M02_DC_train.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\train\02_M01_DC_train.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\train\02_M02_DC_train.csv
- C:\semi\phm_data_challenge_2018\phm_data_challenge_2018\train\03_M01_DC_train.csv
- ...

### 장비 센서 샘플 (01_M01_DC_train.csv, 앞 20만 행)

- shape: (200000, 24)
- 결측 없음

|                         |           mean |             std |          min |            max |
|:------------------------|---------------:|----------------:|-------------:|---------------:|
| time                    |    4.83237e+06 |     1.06214e+06 |  3.28311e+06 |    6.8273e+06  |
| stage                   |   20.434       |    24.1681      |  0           |  119           |
| Lot                     | 1674.03        |  1194.85        |  1           | 4049           |
| runnum                  |    1.06065e+07 | 65034.7         |  1.05116e+07 |    1.07275e+07 |
| recipe                  |    2.3367      |     2.3889      |  0           |   31           |
| recipe_step             |    3.7997      |     3.0742      |  1           |   29           |
| IONGAUGEPRESSURE        |   -0.0098      |     0.9532      | -1.3573      |    1.2866      |
| ETCHBEAMVOLTAGE         |   -0.0065      |     0.9653      | -1.1284      |    1.7204      |
| ETCHBEAMCURRENT         |    0.0062      |     0.9719      | -1.1543      |    3.2732      |
| ETCHSUPPRESSORVOLTAGE   |    0.0894      |     1.0191      | -1.1885      |    1.4205      |
| ETCHSUPPRESSORCURRENT   |    0.1543      |     1.088       | -1.1458      |   20.3701      |
| FLOWCOOLFLOWRATE        |    0.0101      |     0.993       | -1.4495      |    1.7086      |
| FLOWCOOLPRESSURE        |    0.0309      |     0.6333      | -1.2189      |    0.8618      |
| ETCHGASCHANNEL1READBACK |    0.021       |     0.9871      | -1.3643      |    1.3971      |
| ETCHPBNGASREADBACK      |    0.0229      |     0.9866      | -1.5088      |    2.5624      |
| FIXTURETILTANGLE        |   -0.055       |     0.7972      | -1.0541      |    1.1709      |
| ROTATIONSPEED           |   -0.168       |     0.3963      | -0.2039      |    4.2138      |
| ACTUALROTATIONANGLE     |    0.0418      |     0.7453      | -0.1525      |    4.7672      |
| FIXTURESHUTTERPOSITION  |    0.5763      |     1.5029      |  0           |  255           |
| ETCHSOURCEUSAGE         |   -0.6501      |     0.8299      | -1.6793      |    0.3302      |
| ETCHAUXSOURCETIMER      |    0.0671      |     0.188       | -0.2578      |    0.4029      |
| ETCHAUX2SOURCETIMER     |   -0.0227      |     1.266       | -1.5906      |    1.4702      |
| ACTUALSTEPDURATION      |   -0.0232      |     0.8324      | -0.8475      |    4.5399      |

### 고장 라벨 (전체 장비)

- shape: (1236, 4)
- 결측 없음

|      |        mean |         std |         min |         max |
|:-----|------------:|------------:|------------:|------------:|
| time | 2.17017e+07 | 1.09091e+07 | 3.32615e+06 | 4.56783e+07 |
