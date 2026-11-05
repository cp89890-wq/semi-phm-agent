"""데이터 수령 안내 + 압축 해제 + 해시 기록.

원본 호스트가 자동 다운로드를 막거나 링크가 바뀌는 경우가 있어
zip은 브라우저로 직접 받고, 이 스크립트는 풀기·검증만 한다.

사용:
    python scripts/download_data.py                 # 안내 출력
    python scripts/download_data.py cmp  <zip경로>  # data/raw/phm2016 에 풀기
    python scripts/download_data.py ionmill <zip경로>
"""
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

SOURCES = {
    "cmp": {
        "dest": RAW / "phm2016",
        "links": [
            "Kaggle (test 정답 포함): https://www.kaggle.com/datasets/markshizhe/cmp-data-set",
            "Internet Archive 원본: https://web.archive.org/web/20180413091420if_/"
            "https://www.phmsociety.org/sites/phmsociety.org/files/"
            "2016%20PHM%20DATA%20CHALLENGE%20CMP%20DATA%20SET.zip",
        ],
    },
    "ionmill": {
        "dest": RAW / "phm2018",
        "links": [
            "PHM Society 공식: https://drive.google.com/open?id=15Jx9Scq9FqpIGn8jbAQB_lcHSXvIoPzb",
            "NASA DashLink 미러: https://c3.ndc.nasa.gov/dashlink/projects/95/resources/",
        ],
    },
}


def sha256_head(path: Path, n: int = 12) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:n]


def extract(name: str, zip_path: Path) -> None:
    dest = SOURCES[name]["dest"]
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest)
    print(f"[ok] {zip_path.name} -> {dest}")
    print(f"     sha256: {sha256_head(zip_path)}  (data/README.md 수령 기록에 적을 것)")
    files = sorted(p.relative_to(dest) for p in dest.rglob("*") if p.is_file())
    print(f"     files: {len(files)}")
    for p in files[:15]:
        print("      ", p)
    if len(files) > 15:
        print("       ...")


def main(argv: list[str]) -> None:
    if len(argv) < 3:
        print("zip은 아래 링크에서 브라우저로 받은 뒤 이 스크립트로 푼다.\n")
        for name, s in SOURCES.items():
            print(f"[{name}] -> {s['dest'].relative_to(ROOT)}")
            for link in s["links"]:
                print("   ", link)
            print()
        print("예: python scripts/download_data.py cmp ~/Downloads/cmp-data-set.zip")
        return
    name, zip_path = argv[1], Path(argv[2]).expanduser()
    if name not in SOURCES:
        sys.exit(f"알 수 없는 이름: {name} (cmp | ionmill)")
    if not zip_path.exists():
        sys.exit(f"파일 없음: {zip_path}")
    extract(name, zip_path)


if __name__ == "__main__":
    main(sys.argv)
