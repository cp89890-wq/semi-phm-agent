"""경로·시드 등 전역 설정. 실험 재현성을 위해 시드는 여기서만 정한다."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

CMP_DIR = RAW / "phm2016"
IONMILL_DIR = RAW / "phm2018"

SEED = 42
