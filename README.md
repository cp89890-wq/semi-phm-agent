# semi-phm-agent

반도체 장비·공정 데이터 분석 에이전트.
공개 PHM 챌린지 데이터 두 건을 같은 프레임워크로 분석한다.

| 케이스 | 데이터 | 과제 | 직무 연결 |
|---|---|---|---|
| CMP 가상계측 | PHM 2016 | 장비 센서 시계열 → 웨이퍼 재료 제거율(MRR) 회귀 | 공정 엔지니어 (VM, 소모품 관리) |
| 이온밀 고장 예지 | PHM 2018 | 장비 센서 시계열 → flowcool 고장 검출·잔여시간 예측 | CS/장비 엔지니어 (FDC, 예지보전) |

분석 자체는 통계·ML 코드가 수행하고, LLM 에이전트는 **어떤 분석을 할지 고르고 결과를 공정 언어로 해석**하는 역할만 맡는다.
에이전트가 낸 원인 가설은 실제 중요 변수와 비교해 정량 평가한다.

## 결과 요약

> TODO: 완료 후 docs/benchmarks.md의 표를 여기로 복사

| 케이스 | 지표 | 선행 연구 | 본 결과 |
|---|---|---|---|
| CMP | RMSE (low wear / high wear) | 8.18 / 3.97 (PCA30, Lee 2025) | – / – |
| 이온밀 | 챌린지 점수 / 고장 분류 F1 | – | – / – |
| 에이전트 | 원인 변수 Top-5 일치율 | – | – |

## 구조

```
data/raw/            원본 zip 풀어둔 곳 (git 제외)
src/semi_phm/
  loaders/           데이터셋별 로더 → 공통 DataFrame 규격
  tools/             분석 함수 (SPC, 특징추출, 이상점수, 평가). 전부 JSON 반환
  agent/             LLM 에이전트: tools/의 함수를 도구로 호출
experiments/         케이스별 베이스라인 스크립트 (재현 진입점)
eval/                에이전트 평가셋 (질문 + 정답 변수)
docs/                결정 기록, 실패 기록, 벤치마크, 일정
```

## 실행

```bash
pip install -r requirements.txt
python scripts/download_data.py        # 데이터 받는 법 안내 + 압축 해제
python scripts/run_eda.py cmp          # 1차 EDA
python experiments/cmp_baseline.py     # 벤치마크 표 재현
```

## 기록

- [docs/decisions.md](docs/decisions.md) — 무엇을 왜 선택했나
- [docs/failures.md](docs/failures.md) — 틀린 것과 고친 것 (에이전트 포함)
- [docs/benchmarks.md](docs/benchmarks.md) — 선행 연구와 같은 지표로 비교
- [docs/plan.md](docs/plan.md) — 일정과 손절 규칙
