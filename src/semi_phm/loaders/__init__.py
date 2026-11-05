"""데이터셋별 로더.

규약: 각 모듈은 다음 세 함수를 제공한다.
    list_files()  -> list[Path]           원본 파일 목록
    load_sample() -> dict[str, DataFrame] EDA용 대표 테이블 (이름 -> DF)
    load()        -> 정식 로딩 (케이스별 반환 형태는 모듈 docstring 참고)
"""
