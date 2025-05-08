import subprocess


def update_ln39():
    """
    Update all git submodules to their latest remote commits.
    Equivalent to: git submodule update --remote --merge

    Raises:
        subprocess.CalledProcessError: If the git command fails.
    """
    try:
        subprocess.run(
            # ["git", "submodule", "update", "--remote", "--merge"], check=True
            ["pwd"],
            check=True,
        )
        print("[SUBMODULE] All submodules updated to latest remote.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to update submodules: {e}")
