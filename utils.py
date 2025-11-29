from types import SimpleNamespace

from .env_utils import env_equals, env_exists, get_env
from .file_utils import backup
from .git_utils import clone_repo, pull_repo, update_ln39, init_submodules

from .M import M
from .os_utils import get_os_name, path_for


def _lnM(dotfiles: list[M]):
    for dotfile in dotfiles:
        if not dotfile.enabled:
            continue
        # 检查
        if not dotfile.preflight():
            print()
            continue

        opts = SimpleNamespace(
            src=dotfile.source,
            dest=dotfile.destination,
            basedir=dotfile.basedir,
        )

        # ln 前函数
        if callable(dotfile.before_ln):
            try:
                dotfile.before_ln(opts)
            except Exception as e:
                print("before_ln failed:", e)

        dotfile.ln()

        # ln 后函数
        if callable(dotfile.after_ln):
            try:
                dotfile.after_ln(opts)
            except Exception as e:
                print("after_ln failed:", e)

        print()


init = False


def ln(dotfiles: list[M]):
    global init
    if dotfiles:
        if not init:
            basedir = dotfiles[0].basedir
            init_submodules(basedir)
            init = True

    _lnM(dotfiles)


__all__ = [
    "path_for",
    "get_os_name",
    "get_env",
    "env_equals",
    "env_exists",
    "backup",
    "update_ln39",
    "clone_repo",
    "pull_repo",
]
