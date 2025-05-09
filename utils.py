from .env_utils import env_equals, env_exists, get_env
from .file39 import File39
from .file_utils import backup, check_parent_dir
from .git_utils import clone_repo, init_ln39, pull_repo, update_ln39
from .ln import e9ln
from .os_utils import get_linux_name, get_os_name, path_by_os

# TODO:
# if_git_repo


def ln(dotfiles: list[File39]):
    e9ln(dotfiles)


__all__ = [
    "path_by_os",
    "get_os_name",
    "get_env",
    "env_equals",
    "env_exists",
    "get_linux_name",
    "backup",
    "check_parent_dir",
    "update_ln39",
    "init_ln39",
    "clone_repo",
    "pull_repo",
]
