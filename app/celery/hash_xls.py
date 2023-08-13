import hashlib
from pathlib import Path


def calculate_file_hash() -> str:
    with Path("./app/admin/Menu.xlsx").open("rb") as f:
        hasher = hashlib.sha256()
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def read_hash() -> str:
    with Path("./app/admin/hash").open("r") as f:
        return f.read()


def write_hash(hash_summ: str) -> None:
    with Path("./app/admin/hash").open("w") as f:
        f.write(hash_summ)
