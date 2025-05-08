from .file39 import File39


def e9ln(dotfiles: list[File39]):
    for dotfile in dotfiles:
        if not dotfile.enabled:
            continue
        if not dotfile.preflight():
            print()
            continue

        if callable(dotfile.before_ln):
            dotfile.before_ln()

        dotfile.ln()

        if callable(dotfile.after_ln):
            dotfile.after_ln()
        print()
