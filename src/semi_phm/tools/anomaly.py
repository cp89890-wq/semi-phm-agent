"""이상 점수와 그룹 간 비교."""
import numpy as np
import pandas as pd
from scipy import stats


def zscore_anomaly(x: pd.Series, window: int = 200) -> dict:
    """이동 평균·표준편차 기준 z-score로 각 시점의 이상 점수를 내고 상위 지점을 돌려준다."""
    x = pd.Series(x).astype(float)
    mu = x.rolling(window, min_periods=10).mean()
    sd = x.rolling(window, min_periods=10).std().replace(0, np.nan)
    z = ((x - mu) / sd).abs()
    top = z.dropna().sort_values(ascending=False).head(20)
    return {
        "max_z": float(z.max()) if z.notna().any() else None,
        "top_idx": [int(i) for i in top.index],
        "top_z": [round(float(v), 2) for v in top.values],
        "frac_over_3": float((z > 3).mean()),
    }


def compare_groups(df: pd.DataFrame, label_col: str, value_cols: list[str]) -> dict:
    """두 그룹(예: 정상/불량, 고장 전/정상)에서 각 변수의 분포 차이를 검정하고 효과크기 순으로 정렬한다."""
    labels = df[label_col].unique()
    if len(labels) != 2:
        raise ValueError(f"{label_col} 은 두 값이어야 한다: {labels}")
    a, b = (df[df[label_col] == l] for l in labels)
    out = []
    for c in value_cols:
        xa, xb = a[c].dropna(), b[c].dropna()
        if len(xa) < 3 or len(xb) < 3:
            continue
        pooled = np.sqrt((xa.var(ddof=1) + xb.var(ddof=1)) / 2) or np.nan
        d = (xa.mean() - xb.mean()) / pooled if pooled else np.nan
        p = stats.mannwhitneyu(xa, xb, alternative="two-sided").pvalue
        out.append({"var": c, "cohen_d": float(d), "p_value": float(p),
                    "mean_a": float(xa.mean()), "mean_b": float(xb.mean())})
    out.sort(key=lambda r: -abs(r["cohen_d"]) if np.isfinite(r["cohen_d"]) else 0)
    return {"group_a": str(labels[0]), "group_b": str(labels[1]), "ranked": out}
