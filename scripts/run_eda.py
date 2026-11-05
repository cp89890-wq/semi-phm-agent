"""1차 EDA: 파일 구조, 행·열 수, 결측률, 수치 컬럼 요약을 출력한다.

사용:
    python scripts/run_eda.py cmp
    python scripts/run_eda.py ionmill

결과는 outputs/eda_<name>.md 에도 저장한다. 데이터를 처음 받은 날 돌려서
docs/decisions.md 첫 항목("이 데이터로 뭘 보여줄지")의 근거로 쓴다.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from semi_phm.loaders import cmp, ionmill  # noqa: E402

LOADERS = {"cmp": cmp, "ionmill": ionmill}


def describe(df: pd.DataFrame, title: str) -> str:
    lines = [f"### {title}", "", f"- shape: {df.shape}"]
    na = df.isna().mean().sort_values(ascending=False)
    na = na[na > 0]
    if len(na):
        lines.append(f"- 결측 있는 컬럼 {len(na)}개 (상위 5): "
                     + ", ".join(f"{c} {v:.1%}" for c, v in na.head().items()))
    else:
        lines.append("- 결측 없음")
    num = df.select_dtypes("number")
    if len(num.columns):
        desc = num.describe().T[["mean", "std", "min", "max"]]
        lines += ["", desc.round(4).to_markdown()]
    return "\n".join(lines) + "\n"


def main(name: str) -> None:
    mod = LOADERS[name]
    files = mod.list_files()
    if not files:
        sys.exit(f"data/raw 에 {name} 데이터가 없다. scripts/download_data.py 참고.")
    out = [f"# EDA — {name}", "", f"파일 {len(files)}개", ""]
    for p in files[:10]:
        out.append(f"- {p}")
    if len(files) > 10:
        out.append("- ...")
    out.append("")
    sample = mod.load_sample()
    for title, df in sample.items():
        out.append(describe(df, title))
    text = "\n".join(out)
    print(text)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / f"eda_{name}.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in LOADERS:
        sys.exit("사용: python scripts/run_eda.py (cmp|ionmill)")
    main(sys.argv[1])
