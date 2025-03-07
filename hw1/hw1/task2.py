import sys
from typing import List, TextIO

import click
from click.core import Context


@click.command()
@click.argument("files", nargs=-1, type=click.File("r"), required=False)
def tail(files: List[TextIO]) -> None:
    num_lines = 10
    if not files:
        files = [sys.stdin]
        num_lines = 17

    for i, file in enumerate(files):
        if len(files) > 1:
            if i > 0:
                print()
            print(f"==> {file.name} <==")

        lines = file.readlines()

        output = "".join(lines[-num_lines:])
        if lines and not lines[-1]:
            output += "\n"

        print(output, end="")


if __name__ == "__main__":
    tail()
