def printr(
    msg: str,
    tag: str = "",
):
    if tag == "":
        text = msg
    else:
        label = f"[{tag}]".ljust(13)
        text = f"{label}: {msg}"

    print(f"\033[91m{text}\033[0m")


def printg(
    msg: str,
    tag: str = "",
):
    if tag == "":
        text = msg
    else:
        label = f"[{tag}]".ljust(13)
        text = f"{label}: {msg}"
    print(f"\033[92m{text}\033[0m")


def printy(
    msg: str,
    tag: str = "",
):
    if tag == "":
        text = msg
    else:
        tag = f"[{tag}]".ljust(13)
        text = f"{tag}: {msg}"
    print(f"\033[93m{text}\033[0m")
