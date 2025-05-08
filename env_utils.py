import os


def get_env(env_name: str) -> str:
    """
    Retrieve the value of the given environment variable.

    Args:
        env_name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable, or an empty string if not set.
    """
    return os.getenv(env_name, default="")


def env_exists(env_name: str) -> bool:
    """
    Check if a given environment variable is set.

    Args:
        env_name (str): The name of the environment variable.

    Returns:
        bool: True if the environment variable exists, False otherwise.
    """
    return env_name in os.environ


def env_equals(env_name: str, expected_value: str) -> bool:
    """
    Check if a given environment variable is set and equals a specific value.

    Args:
        env_name (str): The name of the environment variable.
        expected_value (str): The value to compare against.

    Returns:
        bool: True if the variable exists and matches the expected value, False otherwise.
    """
    return os.getenv(env_name) == expected_value
