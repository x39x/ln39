from .env_utils import env_equals, env_exists, get_env
from .file39 import File39
from .file_utils import backup, check_parent_dir
from .ln import e9ln
from .os_utils import path_by_os, get_linux_name, get_os_name
from .git_utils import update_ln39, clone_repo, pull_repo

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
    "clone_repo",
    "pull_repo",
]
