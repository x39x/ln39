import subprocess
from os.path import expandvars
from pathlib import Path

from ._cprint import printg, printr, printy
from .file_utils import backup


def init_submodules(repo_path):
    """
    Initialize the submodules of a Git repository.

    This function checks whether the target repository contains submodules,
    determines whether any submodule is uninitialized or out of sync,
    and performs a recursive initialization if necessary.

    Args:
        repo_path (str | Path):
            Absolute or user-expanded path to the Git repository.

    Returns:
        None

    Raises:
        ValueError:
            - The provided path is not a Git repository.
        RuntimeError:
            - Failed to obtain submodule status.
            - Failed to initialize submodules.
    """
    repo = Path(expandvars(str(repo_path))).expanduser().resolve()

    if not (repo / ".git").exists():
        raise ValueError(f"{repo} is not a git repository")

    def run_git(args: list[str]):
        return subprocess.run(
            ["git"] + args,
            cwd=str(repo),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    # 查看 submodule 状态
    status = run_git(["submodule", "status", "--recursive"])
    if status.returncode != 0:
        raise RuntimeError(f"Failed to check submodule status: {status.stderr.strip()}")

    #  判断是否存在未初始化或未同步的 submodule
    needs_init = any(
        line.strip().startswith(("-", "+")) for line in status.stdout.splitlines()
    )

    if not needs_init:
        return  # 所有 submodule 均已初始化

    # 初始化 submodule
    printg(f"Initializing submodules for {repo}", "SUBMODULE")

    result = run_git(["submodule", "update", "--init", "--recursive"])
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to initialize submodules for {repo}: {result.stderr}"
        )

    printg(f"Submodules initialized for {repo}", "SUBMODULE")


def clone_repo(
    repo_url,
    target_dir,
    depth=1,
):
    """
    Clone a git repository to a target directory.

    Args:
        repo_url (str): Git repository URL.
        target_dir (Path | str): Path to clone into.
        depth (int): Shallow clone depth. Default is 1.

    Raises:
        RuntimeError: If git command fails.
    """
    target = Path(expandvars(str(target_dir))).expanduser().resolve()

    if target.exists():
        printy(f"Backup existing directory: {target}", "BACKUP")
        backup(target)

    target.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["git", "clone", "--depth", str(depth), repo_url, str(target)]
    try:
        printg(f"Cloning {repo_url} --> {target}", "CLONE")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git clone failed: {e}")


def pull_repo(repo_path):
    """
    Pull the latest changes in the specified Git repository.

    Args:
        repo_path (Path | str): Path to the local Git repository.

    Raises:
        RuntimeError if the pull operation fails.
    """
    repo_path = Path(expandvars(str(repo_path))).expanduser().resolve()
    if not (repo_path / ".git").exists():
        raise RuntimeError(f"'{repo_path}' is not a valid Git repository.")

    try:
        printg(f"Pulling in '{repo_path}'...", "INFO")
        subprocess.run(
            ["git", "-C", str(repo_path), "pull"],
            check=True,
            capture_output=True,
            text=True,
        )
        printg("Pull completed.", "SUCCESS")
    except subprocess.CalledProcessError as e:
        printr(f"{e.stderr.strip()}", "ERROR")
        raise RuntimeError("Git pull failed") from e


def update_ln39():
    """
    Update all git submodules to their latest remote commits.
    Equivalent to: git submodule update --remote --merge

    Raises:
        subprocess.CalledProcessError: If the git command fails.
    """
    try:
        subprocess.run(
            ["git", "submodule", "update", "--remote", "--rebase"], check=True
        )
        printg("All submodules updated to latest remote.", "SUBMODULE")
    except subprocess.CalledProcessError as e:
        printr(f"Failed to update submodules: {e}", "ERROR")
