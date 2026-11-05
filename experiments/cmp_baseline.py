"""PHM 2016 CMP 베이스라인.

웨이퍼별 특징(tools/cmp_features) → LightGBM 회귀 → 챔버별 RMSE.
분할은 시간순(앞 80% 학습, 뒤 20% 검증)이 기본이고, 비교용으로 랜덤 분할도 같이 낸다.
두 결과의 차이가 "시간 누수" 의 크기다 (docs/failures.md).

실행:
    python experiments/cmp_baseline.py
출력:
    outputs/cmp_baseline_results.md   (benchmarks.md 에 옮겨 적을 표)
    outputs/cmp_baseline_pred.csv     (검증 예측값)
    outputs/cmp_baseline_importance.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from semi_phm.config import SEED  # noqa: E402
from semi_phm.loaders import cmp  # noqa: E402
from semi_phm.tools.cmp_features import build_dataset  # noqa: E402
from semi_phm.tools.evaluate import rmse  # noqa: E402

META = [cmp.WAFER_ID, cmp.STAGE, "t_start", cmp.TARGET]


def make_model():
    try:
        import lightgbm as lgb
        return lgb.LGBMRegressor(n_estimators=600, learning_rate=0.03, num_leaves=15,
                                 min_child_samples=10, subsample=0.8, subsample_freq=1,
                                 colsample_bytree=0.8, random_state=SEED, verbose=-1)
    except ImportError:
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor(n_estimators=400, random_state=SEED, n_jobs=-1)


def split_time(df: pd.DataFrame, frac: float = 0.8):
    cut = df["t_start"].quantile(frac)
    return df[df["t_start"] <= cut].index, df[df["t_start"] > cut].index


def split_random(df: pd.DataFrame, frac: float = 0.8):
    rng = np.random.RandomState(SEED)
    idx = rng.permutation(df.index.values)
    n = int(len(idx) * frac)
    return pd.Index(idx[:n]), pd.Index(idx[n:])


def fit_eval(df: pd.DataFrame, tr, te, label: str) -> tuple[dict, pd.DataFrame, pd.Series]:
    X = df.drop(columns=META)
    X[cmp.STAGE] = (df[cmp.STAGE] == "B").astype(int)
    y = df[cmp.TARGET].values
    m = make_model()
    m.fit(X.loc[tr], y[tr])
    pred = m.predict(X.loc[te])
    out = {"split": label, "n_train": len(tr), "n_val": len(te), "rmse_all": rmse(y[te], pred)}
    for ch in sorted(df["chamber"].unique()):
        mask = (df.loc[te, "chamber"] == ch).values
        if mask.sum() >= 5:
            out[f"rmse_ch{ch}"] = rmse(y[te][mask], pred[mask])
            out[f"n_ch{ch}"] = int(mask.sum())
    # 비교 기준: 챔버 평균만 쓰는 모델 (센서가 얼마나 더 설명하는가)
    ch_mean = df.loc[tr].groupby("chamber")[cmp.TARGET].mean()
    naive = df.loc[te, "chamber"].map(ch_mean).fillna(y[tr].mean()).values
    out["rmse_naive_chamber_mean"] = rmse(y[te], naive)
    imp = pd.Series(getattr(m, "feature_importances_", np.zeros(X.shape[1])), index=X.columns)
    pred_df = df.loc[te, [cmp.WAFER_ID, cmp.STAGE, "chamber", "t_start", cmp.TARGET]].copy()
    pred_df["pred"] = pred
    pred_df["split"] = label
    return out, pred_df, imp


def main() -> None:
    df = build_dataset()
    print(f"웨이퍼 {len(df)}개 (이상치 {df.attrs['n_outlier_removed']}건 제외), 특징 {df.shape[1] - len(META)}개")
    results, preds, imps = [], [], {}
    for label, splitter in [("time", split_time), ("random", split_random)]:
        tr, te = splitter(df)
        r, p, imp = fit_eval(df, tr, te, label)
        results.append(r); preds.append(p); imps[label] = imp
        print(f"[{label:6s}] n_val={r['n_val']}  RMSE all={r['rmse_all']:.3f}  "
              + "  ".join(f"ch{c}={r[f'rmse_ch{c}']:.3f}(n={r[f'n_ch{c}']})" for c in (123, 456) if f"rmse_ch{c}" in r)
              + f"  | naive(chamber mean)={r['rmse_naive_chamber_mean']:.3f}")

    out = ROOT / "outputs"; out.mkdir(exist_ok=True)
    res = pd.DataFrame(results)
    md = ["# CMP 베이스라인 결과", "",
          f"웨이퍼 {len(df)}개, 이상치 {df.attrs['n_outlier_removed']}건 제외, LightGBM, 시드 {SEED}", "",
          res.round(3).to_markdown(index=False), "",
          "## 특징 중요도 상위 15 (시간순 분할 모델)", "",
          imps["time"].sort_values(ascending=False).head(15).round(0).to_markdown()]
    (out / "cmp_baseline_results.md").write_text("\n".join(md), encoding="utf-8")
    pd.concat(preds).to_csv(out / "cmp_baseline_pred.csv", index=False)
    pd.DataFrame(imps).to_csv(out / "cmp_baseline_importance.csv")
    print(f"\n저장: {out / 'cmp_baseline_results.md'}")


if __name__ == "__main__":
    main()
