import inspect
from pathlib import Path
from os.path import (
    expanduser,
    expandvars,
)

from ._cprint import printg, printy, printr
from .file_utils import backup


class M:
    def __init__(
        self,
        src: str,
        dest: str,
        enabled: bool = True,
        before_ln=None,
        after_ln=None,
    ):
        # 获取 dotfile 绝对路径
        caller_frame = inspect.stack()[1]
        caller_abs_path = Path(caller_frame.filename).resolve().parent
        destination = Path(expandvars(dest)).expanduser().absolute()

        self.basedir = caller_abs_path
        self.source = Path(expandvars(expanduser(src)))
        self.destination = destination

        self.enabled = enabled
        self.before_ln = before_ln
        self.after_ln = after_ln

    # 配置文件源目录绝对路径
    @property
    def source_abs(self) -> Path:
        abs_path = self.source
        if not abs_path.is_absolute():
            abs_path = self.basedir / abs_path
        return abs_path.resolve()

    # 检查目标路径是否有软链接或其他情况
    def _check_symlink(self) -> bool:
        should_link = True
        dest = self.destination
        if dest.is_symlink():
            # 可能是死链接
            if not dest.exists():
                printy(f"Symlink target missing: {dest}", "DANGLING")
                backup(dest)
            else:
                current_target_abs = Path(dest).readlink().resolve()
                # 检查是否为正确的软链接
                if current_target_abs == self.source_abs:
                    printg(f"{self.source_abs} --> {dest}", "LINKED")
                    should_link = False
                else:
                    printy(
                        f"Symlink to wrong target: {current_target_abs} --> {dest}",
                        "CONFLICT",
                    )
                    backup(dest)
        elif dest.exists():
            # 目标路径存在其他文件，备份
            printy(f"Path exists: {dest}", "WARN")
            backup(dest)
        return should_link

    # ln 前检查
    def preflight(self) -> bool:
        # 确保目标路径文件夹都存在
        dest_dir = self.destination.parent
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
            printr(dest_dir, "MKDIR")
        src = self.source_abs
        # 确保配置文件存在
        if not src.exists():
            printy(f"config file {src} does not exist", "WARN")
            return False
        return self._check_symlink()

    def ln(self):
        src = self.source_abs
        dst = self.destination
        dst.symlink_to(src, target_is_directory=src.is_dir())

        printg(
            f"{str(self.source_abs).ljust(25)} --> {self.destination}",
            "SUCCESSFUL",
        )
