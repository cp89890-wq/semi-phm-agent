"""PHM 2018 이온밀 베이스라인: 고장 전 구간 라벨링 → 센서 통계 → 고장 분류.

TODO (데이터 받은 뒤, 순서대로):
  1. 고장 시각 기준으로 "고장 전 H시간 구간 = 1, 나머지 = 0" 라벨 생성. H 는 결정 사항 → decisions.md
  2. 레시피/스텝 전환을 이상으로 오인하지 않도록 recipe, recipe_step 으로 구간 분리
  3. 장비 단위 분할(GroupKFold by tool) — 같은 장비가 train/test 에 섞이면 누수
  4. 분류 F1 + 챌린지 점수(tools.evaluate.phm2018_score) 둘 다 보고

LLM 에이전트는 이 스크립트가 만든 특징/모델 결과를 도구로 호출한다. 여기서 LLM 쓰지 않는다.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from semi_phm.loaders import ionmill  # noqa: E402


def main() -> None:
    data = ionmill.load()
    for tool, d in data.items():
        n_f = 0 if d["faults"] is None else len(d["faults"])
        print(f"{tool}: 센서 {len(d['sensor']):,} 행, 고장 {n_f} 건")
    # TODO 1~4


if __name__ == "__main__":
    main()
