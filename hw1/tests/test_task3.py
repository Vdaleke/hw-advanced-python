import os
import shutil
import subprocess

import pytest
from click.testing import CliRunner

from hw1.task3 import wc


def test_wc_single_file():
    if shutil.which("wc") is None:
        pytest.skip("'wc' command not available")

    runner = CliRunner()

    for filename in os.listdir("tests/data"):
        test_file = os.path.join("tests/data", filename)

        if os.path.isfile(test_file):
            expected_output = subprocess.check_output(["wc", test_file]).decode("utf-8")

            result = runner.invoke(wc, [test_file])

            assert result.exit_code == 0
            assert result.output == expected_output, f"Failed on file: {filename}"


def test_wc_multiple_files():
    if shutil.which("wc") is None:
        pytest.skip("'wc' command not available")

    runner = CliRunner()

    file_list = [
        os.path.join("tests/data", filename)
        for filename in os.listdir("tests/data")
        if os.path.isfile(os.path.join("tests/data", filename))
    ]

    expected_output = subprocess.check_output(["wc"] + file_list).decode("utf-8")

    result = runner.invoke(wc, file_list)

    assert result.exit_code == 0
    assert result.output == expected_output, "Failed on multiple files"


def test_wc_from_stdin():
    if shutil.which("wc") is None:
        pytest.skip("'wc' command not available")

    runner = CliRunner()
    input_text = "This is a test\nWith multiple lines\nAnd some more text\n"

    expected_output = subprocess.check_output(["wc"], input=input_text.encode()).decode(
        "utf-8"
    )

    result = runner.invoke(wc, input=input_text)

    assert result.exit_code == 0
    assert result.output == expected_output, "Failed on stdin input"


if __name__ == "__main__":
    pytest.main()
