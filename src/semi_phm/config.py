"""경로·시드 등 전역 설정. 실험 재현성을 위해 시드는 여기서만 정한다."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

import os


def _first_existing(*cands: Path) -> Path:
    for c in cands:
        if c.exists():
            return c
    return cands[0]


CMP_DIR = Path(os.environ.get("SEMI_PHM_CMP_DIR", RAW / "phm2016"))
# 이온밀: 환경변수 > data/raw/phm2018 > data/raw/phm_data_challenge_2018 > 저장소 옆 C:\semi 식 위치
IONMILL_DIR = Path(os.environ["SEMI_PHM_IONMILL_DIR"]) if "SEMI_PHM_IONMILL_DIR" in os.environ else _first_existing(
    RAW / "phm2018",
    RAW / "phm_data_challenge_2018",
    ROOT.parent / "phm_data_challenge_2018",
)

SEED = 42
