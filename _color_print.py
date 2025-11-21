def print_red(
    msg: str,
    type: str | None = None,
):
    if type is None:
        text = msg
    else:
        label = f"[{type}]".ljust(13)
        text = f"{label}: {msg}"

    print(f"\033[91m{text}\033[0m")


def print_green(
    msg: str,
    type: str | None = None,
):
    if type is None:
        text = msg
    else:
        label = f"[{type}]".ljust(13)
        text = f"{label}: {msg}"
    print(f"\033[92m{text}\033[0m")


def print_yellow(
    msg: str,
    type: str | None = None,
):
    if type is None:
        text = msg
    else:
        label = f"[{type}]".ljust(13)
        text = f"{label}: {msg}"
    print(f"\033[93m{text}\033[0m")
