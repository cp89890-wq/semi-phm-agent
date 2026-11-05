"""SPC(통계적 공정관리) 도구: 관리도 한계, 관리 이탈 규칙."""
import numpy as np
import pandas as pd


def imr_limits(x: pd.Series) -> dict:
    """개별값-이동범위(I-MR) 관리도의 중심선과 3σ 관리한계를 계산한다."""
    x = pd.Series(x).dropna().astype(float)
    mr = x.diff().abs().dropna()
    mr_bar = mr.mean()
    sigma = mr_bar / 1.128  # d2 for n=2
    return {
        "n": int(len(x)),
        "center": float(x.mean()),
        "ucl": float(x.mean() + 3 * sigma),
        "lcl": float(x.mean() - 3 * sigma),
        "sigma_est": float(sigma),
    }


def out_of_control(x: pd.Series, limits: dict | None = None) -> dict:
    """관리한계 이탈(3σ 밖)과 연속 7점 한쪽 편향(run rule) 지점을 찾는다."""
    x = pd.Series(x).astype(float)
    lim = limits or imr_limits(x)
    beyond = x[(x > lim["ucl"]) | (x < lim["lcl"])]
    side = np.sign(x - lim["center"])
    runs = []
    cur, start = 0, None
    for i, s in enumerate(side):
        if s != 0 and (cur == 0 or s == side.iloc[i - 1]):
            cur += 1
            start = i if cur == 1 else start
        else:
            cur, start = (1, i) if s != 0 else (0, None)
        if cur == 7:
            runs.append(int(x.index[start]))
    return {
        "n_beyond_limits": int(len(beyond)),
        "beyond_idx": [int(i) for i in beyond.index[:50]],
        "run7_start_idx": runs[:50],
        "limits": lim,
    }
