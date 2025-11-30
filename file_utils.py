import shutil
from pathlib import Path
from datetime import datetime
from os.path import expandvars

from ._cprint import printr


def backup(bak_file: Path | str):
    bak_dir = Path.home() / "ln39.bak"
    bak_dir.mkdir(parents=True, exist_ok=True)
    bak_file = Path(expandvars(str(bak_file))).expanduser()

    base_name = bak_file.name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    dest_path = bak_dir / f"{base_name}_{timestamp}"

    printr(f"{bak_file} --> {dest_path}", "BACKUP")
    # shutil move 可以跨分区
    shutil.move(bak_file, dest_path)
