"""PHM 2016 CMP 로더.

파일 구조(원본 zip, 2016-05-17 판):
    CMP-data/training/CMP-training-<nnn>.csv   185개. 웨이퍼 공정 시계열, 25컬럼 (이름 있음)
    CMP-data/test/CMP-test-<nnn>.csv           185개
    CMP-training-removalrate.csv               훈련 정답: WAFER_ID, STAGE, AVG_REMOVAL_RATE
    CMP-test-removalrate.csv                   테스트 정답 자리 ('?')
    CMP-test-removalrate_V3.csv  (Kaggle markshizhe/cmp-data-set 에서 별도 수령) 테스트 실제 정답

컬럼:
    MACHINE_ID, MACHINE_DATA, TIMESTAMP, WAFER_ID, STAGE, CHAMBER,
    USAGE_OF_BACKING_FILM, USAGE_OF_DRESSER, USAGE_OF_POLISHING_TABLE, USAGE_OF_DRESSER_TABLE,
    PRESSURIZED_CHAMBER_PRESSURE, MAIN_OUTER_AIR_BAG_PRESSURE, CENTER_AIR_BAG_PRESSURE,
    RETAINER_RING_PRESSURE, RIPPLE_AIR_BAG_PRESSURE, USAGE_OF_MEMBRANE, USAGE_OF_PRESSURIZED_SHEET,
    SLURRY_FLOW_LINE_A/B/C, WAFER_ROTATION, STAGE_ROTATION, HEAD_ROTATION,
    DRESSING_WATER_STATUS, EDGE_AIR_BAG_PRESSURE

load(split="training"|"test")는 (traj, target) 두 DataFrame을 돌려준다.
    traj   : 해당 split 의 csv 를 이어붙인 긴 형식 (source 컬럼 = 파일명)
    target : 정답 테이블 (test 는 Kaggle V3 파일, 없으면 '?' 파일)
"""
from pathlib import Path

import pandas as pd

from semi_phm.config import CMP_DIR

WAFER_ID = "WAFER_ID"
STAGE = "STAGE"
TARGET = "AVG_REMOVAL_RATE"
KEY_COLS = ["MACHINE_ID", "MACHINE_DATA", "TIMESTAMP", WAFER_ID, STAGE, "CHAMBER"]
USAGE_COLS = ["USAGE_OF_BACKING_FILM", "USAGE_OF_DRESSER", "USAGE_OF_POLISHING_TABLE",
              "USAGE_OF_DRESSER_TABLE", "USAGE_OF_MEMBRANE", "USAGE_OF_PRESSURIZED_SHEET"]
PRESSURE_COLS = ["PRESSURIZED_CHAMBER_PRESSURE", "MAIN_OUTER_AIR_BAG_PRESSURE",
                 "CENTER_AIR_BAG_PRESSURE", "RETAINER_RING_PRESSURE",
                 "RIPPLE_AIR_BAG_PRESSURE", "EDGE_AIR_BAG_PRESSURE"]
SLURRY_COLS = ["SLURRY_FLOW_LINE_A", "SLURRY_FLOW_LINE_B", "SLURRY_FLOW_LINE_C"]
ROTATION_COLS = ["WAFER_ROTATION", "STAGE_ROTATION", "HEAD_ROTATION"]
STATUS_COLS = ["DRESSING_WATER_STATUS"]
SENSOR_COLS = USAGE_COLS + PRESSURE_COLS + SLURRY_COLS + ROTATION_COLS + STATUS_COLS


def _find(pattern: str) -> list[Path]:
    return sorted(CMP_DIR.rglob(pattern)) if CMP_DIR.exists() else []


def list_files() -> list[Path]:
    return _find("*.csv")


def _traj_files(split: str) -> list[Path]:
    return [p for p in _find(f"CMP-{split}-*.csv") if "removalrate" not in p.name.lower()]


def _target_file(split: str) -> Path | None:
    if split == "test":
        v3 = _find("CMP-test-removalrate_V3.csv")
        if v3:
            return v3[0]
    f = _find(f"CMP-{split}-removalrate.csv")
    return f[0] if f else None


def load_target(split: str = "training") -> pd.DataFrame:
    p = _target_file(split)
    if p is None:
        raise FileNotFoundError(f"{split} 정답 파일 없음")
    df = pd.read_csv(p)
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    return df


def load_sample() -> dict[str, pd.DataFrame]:
    out = {}
    train = _traj_files("training")
    if train:
        out[f"training 시계열 샘플 ({train[0].name})"] = pd.read_csv(train[0])
    try:
        out["training removal rate (정답)"] = load_target("training")
    except FileNotFoundError:
        pass
    return out


def load(split: str = "training") -> tuple[pd.DataFrame, pd.DataFrame]:
    frames = []
    for p in _traj_files(split):
        df = pd.read_csv(p)
        df["source"] = p.name
        frames.append(df)
    if not frames:
        raise FileNotFoundError(f"{CMP_DIR} 아래에 CMP-{split}-*.csv 없음")
    traj = pd.concat(frames, ignore_index=True)
    return traj, load_target(split)
