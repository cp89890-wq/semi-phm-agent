"""시계열 → 웨이퍼/구간 단위 특징 요약."""
import numpy as np
import pandas as pd


def summarize_series(x: pd.Series) -> dict:
    """한 시계열을 평균·표준편차·최소·최대·기울기·마지막값으로 요약한다."""
    x = pd.Series(x).dropna().astype(float)
    if len(x) == 0:
        return {k: None for k in ["mean", "std", "min", "max", "slope", "last", "n"]}
    t = np.arange(len(x))
    slope = float(np.polyfit(t, x.values, 1)[0]) if len(x) > 1 else 0.0
    return {
        "mean": float(x.mean()), "std": float(x.std(ddof=0)),
        "min": float(x.min()), "max": float(x.max()),
        "slope": slope, "last": float(x.iloc[-1]), "n": int(len(x)),
    }


def per_group_features(df: pd.DataFrame, group_cols: list[str], value_cols: list[str]) -> pd.DataFrame:
    """그룹(예: WAFER_ID, STAGE)별로 각 센서를 summarize_series 통계로 요약한 표를 만든다."""
    rows = []
    for key, g in df.groupby(group_cols, sort=False):
        key = key if isinstance(key, tuple) else (key,)
        row = dict(zip(group_cols, key))
        for c in value_cols:
            s = summarize_series(g[c])
            for k, v in s.items():
                if k != "n":
                    row[f"{c}__{k}"] = v
        row["n_points"] = len(g)
        rows.append(row)
    return pd.DataFrame(rows)
