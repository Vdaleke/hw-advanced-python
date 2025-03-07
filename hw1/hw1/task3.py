import sys

import click


def process_file(file):
    lines = words = bytes_ = 0
    for line in file:
        lines += 1
        words += len(line.split())
        bytes_ += len(line.encode("utf-8"))
    return lines, words, bytes_


@click.command()
@click.argument("files", nargs=-1, type=click.File("r"), required=False)
def wc(files):
    if not files:
        files = [sys.stdin]

    total_lines = total_words = total_bytes = 0
    multiple_files = len(files) > 1

    for file in files:
        lines, words, bytes_ = process_file(file)
        total_lines += lines
        total_words += words
        total_bytes += bytes_

        if file is sys.stdin:
            print(f"{lines:8d}{words:8d}{bytes_:8d}")
        else:
            print(f"{lines:8d}{words:8d}{bytes_:8d} {file.name}")

    if multiple_files:
        print(f"{total_lines:8d}{total_words:8d}{total_bytes:8d} total")


if __name__ == "__main__":
    wc()
