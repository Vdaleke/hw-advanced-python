import os
import shutil
import subprocess

import pytest
from click.testing import CliRunner

from hw1.task2 import tail


def test_tail_single_file():
    if shutil.which("tail") is None:
        pytest.skip("'tail' command not available")

    runner = CliRunner()

    for filename in os.listdir("tests/data"):
        test_file = os.path.join("tests/data", filename)

        if os.path.isfile(test_file):
            expected_output = subprocess.check_output(["tail", test_file]).decode(
                "utf-8"
            )

            result = runner.invoke(tail, [test_file])

            assert result.exit_code == 0
            assert result.output == expected_output, f"Failed on file: {filename}"


def test_tail_multiple_files():
    if shutil.which("tail") is None:
        pytest.skip("'tail' command not available")

    runner = CliRunner()

    file_list = [
        os.path.join("tests/data", filename)
        for filename in os.listdir("tests/data")
        if os.path.isfile(os.path.join("tests/data", filename))
    ]

    expected_output = subprocess.check_output(["tail"] + file_list).decode("utf-8")

    result = runner.invoke(tail, file_list)

    assert result.exit_code == 0
    assert result.output == expected_output, "Failed on multiple files"


def test_tail_from_stdin():
    if shutil.which("tail") is None:
        pytest.skip("'tail' command not available")

    runner = CliRunner()
    input_text = "\n".join(f"Line {i}" for i in range(1, 30))

    expected_output = subprocess.check_output(
        ["tail", "-n", "17"], input=input_text.encode()
    ).decode("utf-8")

    result = runner.invoke(tail, input=input_text)

    assert result.exit_code == 0
    assert result.output == expected_output, "Failed on stdin input"
