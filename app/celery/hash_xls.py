import hashlib
from pathlib import Path

from app.config import ADMIN_PATH


async def calculate_file_hash(filename: Path) -> str:
    with Path(filename).open("rb") as f:
        hasher = hashlib.sha256()
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


async def read_hash() -> str:
    with ADMIN_PATH.joinpath("hash").open("r") as f:
        return f.read()


async def write_hash(hash_summ: str) -> None:
    with ADMIN_PATH.joinpath("hash").open("w") as f:
        f.write(hash_summ)
