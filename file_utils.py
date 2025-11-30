import shutil
from pathlib import Path
from datetime import datetime
from os.path import expandvars

from ._cprint import printr


def backup(bak_file):
    """
    Backup a file to ~/ln39.bak/ with timestamp.

    Args:
        bak_file (Path | str): Absolute path of the file to backup.

    Behavior:
        - Creates backup directory if it doesn't exist.
        - Appends timestamp to filename to avoid overwrite.
        - Moves the original file to the backup directory.
    """
    bak_dir = Path.home() / "ln39.bak"
    bak_dir.mkdir(parents=True, exist_ok=True)
    bak_file = Path(expandvars(str(bak_file))).expanduser()

    base_name = bak_file.name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    dest_path = bak_dir / f"{base_name}_{timestamp}"

    printr(f"{bak_file} --> {dest_path}", "BACKUP")
    # shutil move 可以跨分区
    shutil.move(bak_file, dest_path)
