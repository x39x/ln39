import subprocess
from os.path import expandvars
from pathlib import Path

from ._cprint import printg, printr
from .file_utils import backup


def init_submodules(repo_path: Path | str):
    """
    init a git repository's submodule

    Args:
        repo_path (str or Path): Git repository absolute path

    Raises:
        TODO
    """
    repo = Path(expandvars(str(repo_path))).expanduser().resolve()

    if not (repo / ".git").exists():
        raise ValueError(f"{repo} is not a git repository")

    def run_git(args):
        return subprocess.run(
            ["git"] + args,
            cwd=str(repo),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    # 检查 submodule 状态
    status = run_git(["submodule", "status", "--recursive"])
    if status.returncode != 0:
        print()
        printr(f"No submodules or failed to check: {status.stderr.strip()}", "WARN")
        return

    # 判断是否有未初始化/未同步的 submodule
    needs_init = any(
        line.strip().startswith(("-", "+")) for line in status.stdout.splitlines()
    )

    if not needs_init:
        return

    # 2. 执行初始化
    printg(f"Initializing submodules for {repo}", "SUBMODULE")

    result = run_git(["submodule", "update", "--init", "--recursive"])
    if result.returncode == 0:
        printg(f"Submodules initialized for {repo}", "SUBMODULE")
    else:
        printr(f"Failed to init submodules for {repo}", "ERROR")
        print(result.stderr)


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


def clone_repo(
    repo_url: Path | str,
    target_dir: str,
    depth: int = 1,
):
    """
    Clone a git repository to a target directory.

    Args:
        repo_url (str): Git repository URL.
        target_dir (str): Path to clone into.
        depth (int): Shallow clone depth. Default is 1.

    Raises:
        RuntimeError: If git command fails.
    """
    target = Path(expandvars(str(target_dir))).expanduser().resolve()

    if target.exists():
        print(f"[WARN] Backup existing directory: {target}")
        backup(target)

    target.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["git", "clone", "--depth", str(depth), repo_url, str(target)]
    try:
        print(f"[CLONE] Cloning {repo_url} --> {target}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git clone failed: {e}")


def pull_repo(repo_path: Path | str):
    """
    Pull the latest changes in the specified Git repository.

    Parameters:
    - repo_path: str. Path to the local Git repository.

    Raises:
    - RuntimeError if the pull operation fails.
    """
    repo_path = Path(expandvars(str(repo_path))).expanduser().resolve()
    if not (repo_path / ".git").exists():
        raise RuntimeError(f"'{repo_path}' is not a valid Git repository.")

    try:
        print(f"[INFO] Pulling in '{repo_path}'...")
        subprocess.run(
            ["git", "-C", str(repo_path), "pull"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("[SUCCESS] Pull completed.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {e.stderr.strip()}")
        raise RuntimeError("Git pull failed") from e
