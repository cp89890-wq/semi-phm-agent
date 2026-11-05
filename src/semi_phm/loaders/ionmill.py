"""PHM 2018 이온밀 식각 장비 로더.

파일 구조(원본 기준):
    train/<tool>.csv             장비 1대 = csv 1개. 24컬럼 (time, Tool, stage, Lot, runnum,
                                 recipe, recipe_step, IONGAUGEPRESSURE, ETCHBEAMVOLTAGE, ...,
                                 FLOWCOOLFLOWRATE, FLOWCOOLPRESSURE, ..., ACTUALSTEPDURATION)
    train/train_faults/<tool>.csv   고장 시각: time, fault_name, stage
    train/train_tff/<tool>.csv      잔여시간(TTF) 예시
    test/<tool>.csv

고장 3종(모두 flowcool 계통):
    "FlowCool Pressure Dropped Below Limit"
    "Flowcool Pressure Too High Check Flowcool Pump"
    "Flowcool leak"

load()는 dict[tool_name -> {"sensor": DF, "faults": DF | None}] 를 돌려준다.
"""
from pathlib import Path

import pandas as pd

from semi_phm.config import IONMILL_DIR

FAULTS = [
    "FlowCool Pressure Dropped Below Limit",
    "Flowcool Pressure Too High Check Flowcool Pump",
    "Flowcool leak",
]
SENSOR_COLS = [
    "IONGAUGEPRESSURE", "ETCHBEAMVOLTAGE", "ETCHBEAMCURRENT",
    "ETCHSUPPRESSORVOLTAGE", "ETCHSUPPRESSORCURRENT",
    "FLOWCOOLFLOWRATE", "FLOWCOOLPRESSURE",
    "ETCHGASCHANNEL1READBACK", "ETCHPBNGASREADBACK",
    "FIXTURETILTANGLE", "ROTATIONSPEED", "ACTUALROTATIONANGLE",
    "FIXTURESHUTTERPOSITION", "ETCHSOURCEUSAGE",
    "ETCHAUXSOURCETIMER", "ETCHAUX2SOURCETIMER", "ACTUALSTEPDURATION",
]


def _train_dir() -> Path | None:
    cands = [p for p in IONMILL_DIR.rglob("train") if p.is_dir()] if IONMILL_DIR.exists() else []
    return cands[0] if cands else None


def list_files() -> list[Path]:
    return sorted(IONMILL_DIR.rglob("*.csv")) if IONMILL_DIR.exists() else []


def _tool_csvs(train: Path) -> list[Path]:
    return sorted(p for p in train.glob("*.csv"))


def load_sample() -> dict[str, pd.DataFrame]:
    out = {}
    train = _train_dir()
    if train is None:
        return out
    tools = _tool_csvs(train)
    if tools:
        out[f"장비 센서 샘플 ({tools[0].name}, 앞 20만 행)"] = pd.read_csv(tools[0], nrows=200_000)
    faults = sorted((train / "train_faults").glob("*.csv")) if (train / "train_faults").exists() else []
    if faults:
        fdf = pd.concat([pd.read_csv(p).assign(tool=p.stem) for p in faults], ignore_index=True)
        out["고장 라벨 (전체 장비)"] = fdf
        print("고장 건수:\n", fdf["fault_name"].value_counts().to_string())
    return out


def load() -> dict[str, dict[str, pd.DataFrame | None]]:
    train = _train_dir()
    if train is None:
        raise FileNotFoundError(f"{IONMILL_DIR} 아래에 train 폴더가 없다")
    data = {}
    for p in _tool_csvs(train):
        fpath = train / "train_faults" / p.name
        data[p.stem] = {
            "sensor": pd.read_csv(p),
            "faults": pd.read_csv(fpath) if fpath.exists() else None,
        }
    return data
