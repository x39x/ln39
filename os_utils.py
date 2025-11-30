import platform
import subprocess
from typing import Optional


def get_os_name():
    """
    Return the base operating system name as detected by Python's platform module.

    Returns:
        str: 'Linux', 'Darwin', 'Windows', etc.
    """
    return platform.system()


def path_for(
    linux: Optional[str] = None,
    macos: Optional[str] = None,
    bsd: Optional[str] = None,
    windows: Optional[str] = None,
) -> str:
    """
    Return path for current OS, supporting only Linux, macOS, Windows.

    Args:
        linux (Optional[str]): Path for Linux.
        macos (Optional[str]): Path for macOS (Darwin).
        bsd (Optional[str]): Path for BSD
        windows (Optional[str]): Path for Windows.

    Returns:
        str: The path corresponding to the detected OS.

    Raises:
        NotImplementedError: If the OS is supported but corresponding path is missing.
    """
    os_name = get_os_name()

    if os_name == "Linux":
        if linux is not None:
            return linux
        raise NotImplementedError("Linux detected but no Linux path provided.")

    elif os_name == "Darwin":
        if macos is not None:
            return macos
        raise NotImplementedError("macOS detected but no macOS path provided.")

    elif os_name == "Windows":
        if windows is not None:
            return windows
        raise NotImplementedError("Windows detected but no Windows path provided.")
    elif os_name in ("FreeBSD", "OpenBSD", "NetBSD", "DragonFly"):
        if bsd is not None:
            return bsd
        raise NotImplementedError("bsd detected but no bsd path provided.")

    else:
        raise NotImplementedError(f"Unsupported OS: {os_name}")


def run_shell_command(command, cwd=None, capture_output=True, check=True, shell=False):
    """
    Execute a shell command and return the result.

    Parameters:
    - command: list or str. The shell command to execute (e.g., ["ls", "-l"] or "ls -l").
    - cwd: str. The working directory in which to run the command.
    - capture_output: bool. Whether to capture stdout and stderr.
    - check: bool. Whether to raise an exception if the command fails.
    - shell: bool. Whether to execute the command through the shell (e.g., `bash -c`).

    Returns:
    - A CompletedProcess object containing stdout, stderr, and the return code.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=check,
            shell=shell,
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"""[ERROR] : {e}
stdout: {e.stdout}")
stderr: {e.stderr}""")
        raise
