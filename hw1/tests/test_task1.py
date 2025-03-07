import os
import shutil
import subprocess

import pytest
from click.testing import CliRunner

from hw1.task1 import number_lines


def test_number_lines():
    if shutil.which("nl") is None:
        pytest.skip("'nl' command not available")

    runner = CliRunner()

    for filename in os.listdir("tests/data"):
        test_file = os.path.join("tests/data", filename)

        if os.path.isfile(test_file):
            expected_output = subprocess.check_output(
                ["nl", "-b", "a", test_file]
            ).decode("utf-8")

            result = runner.invoke(number_lines, [test_file])

            assert result.exit_code == 0
            assert result.output == expected_output, f"Failed on file: {filename}"


# some bug in CliRunner similar to https://github.com/fastapi/typer/discussions/560
# CliRunner do not force replace stdin and function use system stdin ??

# def test_number_lines_from_stdin():
#     if shutil.which("nl") is None:
#         pytest.skip("'nl' command not available")

#     runner = CliRunner()
#     input_text = "This is a test\nWith multiple lines\nAnd more text\n"

#     expected_output = subprocess.check_output(
#         ["nl", "-b", "a"], input=input_text.encode()
#     )
#     print(expected_output.decode())

#     result = runner.invoke(number_lines, input=input_text)

#     assert result.exit_code == 0
#     assert result.output == expected_output.decode(), "Failed on stdin input"
