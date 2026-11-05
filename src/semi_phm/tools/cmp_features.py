"""CMP 웨이퍼별 특징 추출.

EDA(2026-11-05) 반영:
- 압력·슬러리·회전 변수는 웨이퍼 안에서 0 ↔ 값 사이를 오간다 → 0 이 아닌 구간만 요약
- 사용량(USAGE_*) 변수는 웨이퍼 내에서 거의 상수 → 평균 하나
- 챔버(MACHINE_DATA), 시작 시각(TIMESTAMP) 은 메타로 보존
"""
import numpy as np
import pandas as pd

from semi_phm.loaders import cmp

ACTIVE_COLS = cmp.PRESSURE_COLS + cmp.SLURRY_COLS + cmp.ROTATION_COLS


def _active_stats(x: pd.Series) -> dict:
    """0 이 아닌 구간의 평균·표준편차·최대·활성 비율. 전부 0 이면 NaN."""
    x = x.astype(float)
    a = x[x > 0]
    if len(a) == 0:
        return {"mean": np.nan, "std": np.nan, "max": np.nan, "frac": 0.0}
    return {"mean": a.mean(), "std": a.std(ddof=0), "max": a.max(), "frac": len(a) / len(x)}


def wafer_features(traj: pd.DataFrame) -> pd.DataFrame:
    """긴 형식 시계열 → 웨이퍼·스테이지 한 줄 특징 표."""
    rows = []
    for (wid, stage), g in traj.groupby([cmp.WAFER_ID, cmp.STAGE], sort=False):
        r = {cmp.WAFER_ID: wid, cmp.STAGE: stage,
             # 한 웨이퍼는 챔버 1→2→3 또는 4→5→6 을 거친다 (2026-11-05 확인). 그룹으로 표기.
             "chamber": 123 if g["MACHINE_DATA"].iloc[0] <= 3 else 456,
             "t_start": float(g["TIMESTAMP"].min()),
             "n_points": len(g),
             "duration": float(g["TIMESTAMP"].max() - g["TIMESTAMP"].min())}
        for c in cmp.USAGE_COLS:
            r[f"{c}__mean"] = float(g[c].mean())
        for c in ACTIVE_COLS:
            s = _active_stats(g[c])
            for k, v in s.items():
                r[f"{c}__{k}"] = v
        r["DRESSING_WATER_STATUS__frac"] = float(g["DRESSING_WATER_STATUS"].mean())
        rows.append(r)
    return pd.DataFrame(rows)


def build_dataset(outlier_threshold: float = 300.0) -> pd.DataFrame:
    """training 전체 → 특징 + 정답 병합. 제거율 > threshold 는 제외하고 n_outlier 를 attrs 에 기록."""
    traj, target = cmp.load("training")
    feats = wafer_features(traj)
    df = feats.merge(target, on=[cmp.WAFER_ID, cmp.STAGE], how="inner")
    n_out = int((df[cmp.TARGET] > outlier_threshold).sum())
    df = df[df[cmp.TARGET] <= outlier_threshold].reset_index(drop=True)
    df.attrs["n_outlier_removed"] = n_out
    return df
