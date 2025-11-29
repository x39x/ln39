import platform
import subprocess


def get_os_name():
    """
    Return the base operating system name as detected by Python's platform module.

    Returns:
        str: 'Linux', 'Darwin', 'Windows', etc.
    """
    return platform.system()


# TODO: win bsd
def path_for(
    linux: str,
    macos: str,
) -> str:
    """
    Return the platform-specific path based on the current OS.

    Args:
        linux (str): The path to use on Linux systems.
        macos (str): The path to use on macOS systems.

    Returns:
        str: The appropriate path for the detected operating system.

    Raises:
        NotImplementedError: If the platform is not supported.
    """
    os_name = get_os_name()
    if os_name == "Darwin":
        return macos
    elif os_name == "Linux":
        return linux
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
