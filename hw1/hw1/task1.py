import sys
from typing import TextIO

import click


@click.command()
@click.argument("file", type=click.File("r"), default=sys.stdin, required=False)
def number_lines(file: TextIO):
    for line_number, line in enumerate(file, start=1):
        print(f"{line_number:>6}\t{line}", end="")


if __name__ == "__main__":
    number_lines()
