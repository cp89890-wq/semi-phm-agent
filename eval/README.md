# 에이전트 평가셋

`questions.jsonl` 한 줄에 질문 하나. 2단계 시작 전에 50개를 채운다.
정답 변수(`truth_vars`)는 1단계 통계 모델의 특징 중요도·그룹 비교 결과에서 뽑는다.
즉 **정답은 코드가 만들고, 에이전트는 그걸 맞혀야 한다.**

```json
{"id": "cmp-001", "case": "cmp", "query": "WAFER_ID 1234 STAGE A 의 제거율이 낮은 이유는?",
 "context": {"wafer_id": 1234, "stage": "A"},
 "truth_vars": ["USAGE_OF_DRESSER__mean", "PRESSURIZED_CHAMBER_PRESSURE__slope", "..."],
 "truth_note": "드레서 사용량 상위 5% 구간, 고마모"}
```

채점: 에이전트가 지목한 원인 변수 상위 5개와 `truth_vars` 상위 5개의 겹침 비율.
