"""PHM 2016 CMP 베이스라인: 웨이퍼별 특징 요약 → LightGBM 회귀 → 저/고마모 RMSE.

이 스크립트가 docs/benchmarks.md 의 CMP 행을 재현하는 진입점이다.
분할 기준·시드를 바꾸면 반드시 docs/decisions.md 에 기록한다.

TODO (EDA 2026-11-05 반영, outputs/eda_cmp_notes.md 참고):
  1. 제거율 >300 이상치 4건 제외
  2. 챔버(MACHINE_DATA) 2 / 5 별로 RMSE 따로 보고 (논문의 low/high wear 구분과 대응 확인)
  3. 분할: 시간순(TIMESTAMP 기준 앞 80%) — 랜덤 분할 결과도 같이 내서 누수 효과를 failures.md 에
  4. 특징: 압력·슬러리·회전은 0 구간 제외하고 요약 (웨이퍼 안에 여러 단계가 있음)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from semi_phm.config import SEED  # noqa: E402
from semi_phm.loaders import cmp  # noqa: E402
from semi_phm.tools.evaluate import rmse  # noqa: E402
from semi_phm.tools.features import per_group_features  # noqa: E402

COL_MAP: dict[str, str] = {}  # 예: {"x4": "WAFER_ID", "x5": "STAGE", ...}


def main() -> None:
    traj, target = cmp.load()
    if COL_MAP:
        traj = traj.rename(columns=COL_MAP)
    sensor_cols = [c for c in traj.select_dtypes("number").columns
                   if c not in (cmp.WAFER_ID, cmp.STAGE)]
    feats = per_group_features(traj, [cmp.WAFER_ID, cmp.STAGE], sensor_cols)
    df = feats.merge(target, on=[cmp.WAFER_ID, cmp.STAGE], how="inner")
    X = df.drop(columns=[cmp.WAFER_ID, cmp.STAGE, cmp.TARGET])
    y = df[cmp.TARGET].values
    groups = df[cmp.WAFER_ID].values

    try:
        import lightgbm as lgb
        model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.03, random_state=SEED, verbose=-1)
    except ImportError:
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=-1)

    pred = np.zeros_like(y, dtype=float)
    for tr, te in GroupKFold(n_splits=5).split(X, y, groups):
        model.fit(X.iloc[tr], y[tr])
        pred[te] = model.predict(X.iloc[te])

    print(f"전체 RMSE: {rmse(y, pred):.4f}  (n={len(y)})")
    # TODO: 저마모/고마모 분리 후 각각 RMSE → docs/benchmarks.md
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    pd.DataFrame({"y": y, "pred": pred, cmp.WAFER_ID: groups}).to_csv(out / "cmp_cv_pred.csv", index=False)


if __name__ == "__main__":
    main()
