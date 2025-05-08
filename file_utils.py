import shutil
from datetime import datetime
from os import makedirs, path
from os.path import (
    basename,
    dirname,
    expanduser,
)

from ._color_print import print_red


def backup(bak_file: str):
    if not path.exists(bak_file):
        if not path.islink(bak_file):
            return

    home = expanduser("~")
    bak_dir = path.join(home, "ln39.bak")
    makedirs(bak_dir, exist_ok=True)

    base_name = basename(bak_file)
    dest_path = path.join(bak_dir, base_name)

    if path.exists(dest_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        dest_path = path.join(bak_dir, f"{base_name}_{timestamp}")
    print_red(f"[BACKUP]   Moved to backup               : {bak_file} --> {dest_path}")
    shutil.move(bak_file, dest_path)


def check_parent_dir(dest_path: str):
    parent = dirname(dest_path)
    if not path.exists(parent):
        print_red(f"[MKDIR]    Creating missing directory    : {parent}")
        makedirs(parent, exist_ok=True)
