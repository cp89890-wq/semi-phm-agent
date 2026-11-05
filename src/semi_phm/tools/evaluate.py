"""평가 지표. 선행 연구·챌린지와 같은 정의를 쓴다. 정의 출처를 docstring에 남긴다."""
import numpy as np


def rmse(y_true, y_pred) -> float:
    """RMSE. CMP 논문들(Lee 2025 등)의 저마모/고마모 구간별 비교 지표."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def phm2018_score(gt, sub) -> float:
    """PHM 2018 공식 점수 (낮을수록 좋음). gt/sub 는 TTF 배열, 없음은 NaN.
    규칙: 둘 다 숫자 exp(-0.001*GT)*|GT-SUB|; GT만 NaN exp(-0.001*SUB)*SUB;
    SUB만 NaN exp(-0.001*GT)*GT; 둘 다 NaN 0. 셀 평균."""
    gt, sub = np.asarray(gt, float), np.asarray(sub, float)
    s = np.zeros_like(gt)
    both = ~np.isnan(gt) & ~np.isnan(sub)
    s[both] = np.exp(-0.001 * gt[both]) * np.abs(gt[both] - sub[both])
    gt_nan = np.isnan(gt) & ~np.isnan(sub)
    s[gt_nan] = np.exp(-0.001 * sub[gt_nan]) * sub[gt_nan]
    sub_nan = ~np.isnan(gt) & np.isnan(sub)
    s[sub_nan] = np.exp(-0.001 * gt[sub_nan]) * gt[sub_nan]
    return float(s.mean())


def topk_overlap(agent_vars: list[str], true_vars: list[str], k: int = 5) -> dict:
    """에이전트가 지목한 원인 변수 상위 k개와 실제 중요 변수 상위 k개의 겹침 비율."""
    a, t = set(agent_vars[:k]), set(true_vars[:k])
    return {"k": k, "overlap": len(a & t), "ratio": len(a & t) / k if k else 0.0,
            "agent": list(a), "truth": list(t)}
