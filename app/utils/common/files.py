from pathlib import Path


def read_file(file_path: str | Path, mode: str = "r"):
    with open(file_path, mode, encoding="utf-8" if mode == "r" else None) as f:
        data = f.read()
    return data
