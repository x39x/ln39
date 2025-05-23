import subprocess
import os
from pathlib import Path
from .file_utils import backup


def init_ln39():
    try:
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            check=True,
        )
        print("[SUBMODULE] All submodules init")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to init submodules: {e}")


def update_ln39():
    """
    Update all git submodules to their latest remote commits.
    Equivalent to: git submodule update --remote --merge

    Raises:
        subprocess.CalledProcessError: If the git command fails.
    """
    try:
        subprocess.run(
            ["git", "submodule", "update", "--remote", "--merge"], check=True
        )
        print("[SUBMODULE] All submodules updated to latest remote.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to update submodules: {e}")


def clone_repo(
    repo_url: str,
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
    target = Path(os.path.expanduser(target_dir))

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


def pull_repo(repo_path: str):
    """
    Pull the latest changes in the specified Git repository.

    Parameters:
    - repo_path: str. Path to the local Git repository.

    Raises:
    - RuntimeError if the pull operation fails.
    """
    repo_path = Path(repo_path).expanduser().resolve()
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
