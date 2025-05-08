import inspect
from .file_utils import backup, check_parent_dir
from os import path, readlink, symlink
from os.path import (
    abspath,
    dirname,
    expanduser,
    expandvars,
    isabs,
)
from typing import Callable, Optional

from ._color_print import print_green, print_yellow


class File39:
    def __init__(
        self,
        source: str,
        destination: str,
        enabled: bool = True,
        before_ln: Optional[Callable[..., None]] = None,
        after_ln: Optional[Callable[..., None]] = None,
    ):
        caller_frame = inspect.stack()[1]
        caller_abs_path = dirname(abspath(caller_frame.filename))

        destination_abs = abspath(expandvars(expanduser(destination)))

        self.basedir = caller_abs_path
        self.source = source
        self.destination_abs = destination_abs
        self.enabled = enabled
        self.before_ln = before_ln
        self.after_ln = after_ln

    @property
    def source_abs(self) -> str:
        abs_path = expandvars(expanduser(self.source))
        if not isabs(abs_path):
            abs_path = path.join(self.basedir, abs_path)
        return abspath(abs_path)

    def _check_symlink(self) -> bool:
        should_link = True
        dest = self.destination_abs
        if path.islink(dest):
            if not path.exists(dest):
                print_yellow(f"[DANGLING] Symlink target missing        : {dest}")
                backup(dest)
            else:
                current_target_abs = abspath(readlink(dest))
                if current_target_abs == self.source_abs:
                    print_green(
                        f"[LINK]     Symlink already correct       : {self.source_abs} --> {dest}"
                    )
                    should_link = False
                else:
                    print_yellow(
                        f"[CONFLICT] Symlink to wrong target       : {current_target_abs} --> {dest}"
                    )
                    backup(dest)
        elif path.exists(dest):
            print_yellow(f"[WARN]     Path exists but not a symlink : {dest}")
            backup(dest)
        return should_link

    def preflight(self) -> bool:
        check_parent_dir(self.destination_abs)
        return self._check_symlink()

    def ln(self):
        symlink(
            self.source_abs,
            self.destination_abs,
            target_is_directory=path.isdir(self.source_abs),
        )
        print_green(
            f"[DONE]     Linked successfully           : {self.source_abs.ljust(25)} --> {self.destination_abs}"
        )
