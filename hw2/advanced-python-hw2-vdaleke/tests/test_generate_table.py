import pytest

from advanced_python_hw2_vdaleke import generate_table


def test_generate_table_valid_input():
    data = [["Name", "Age", "City"], ["Alice", 25, "London"], ["Bob", 30, "Paris"]]
    expected_output = (
        "\\begin{tabular}{|c|c|c|}\n"
        "\\hline\n"
        "Name & Age & City \\\\\n"
        "Alice & 25 & London \\\\\n"
        "Bob & 30 & Paris \\\\\n"
        "\\hline\n"
        "\\end{tabular}"
    )
    assert generate_table(data) == expected_output


def test_generate_table_single_row():
    data = [["OnlyOneRow"]]
    expected_output = (
        "\\begin{tabular}{|c|}\n"
        "\\hline\n"
        "OnlyOneRow \\\\\n"
        "\\hline\n"
        "\\end{tabular}"
    )
    assert generate_table(data) == expected_output


def test_generate_table_empty_list():
    with pytest.raises(IndexError):
        generate_table([])


def test_generate_table_empty_row():
    with pytest.raises(ValueError, match="Rows must have at least one element"):
        generate_table([[]])


def test_generate_table_incorrect_row_lengths():
    data = [["Name", "Age"], ["Alice", 25, "London"]]
    with pytest.raises(
        ValueError, match="All rows must have the same number of elements"
    ):
        generate_table(data)


def test_generate_table_numbers():
    data = [[1, 2], [3, 4]]
    expected_output = (
        "\\begin{tabular}{|c|c|}\n"
        "\\hline\n"
        "1 & 2 \\\\\n"
        "3 & 4 \\\\\n"
        "\\hline\n"
        "\\end{tabular}"
    )
    assert generate_table(data) == expected_output


def test_generate_table_special_characters():
    data = [["$", "%"], ["_", "&"]]
    expected_output = (
        "\\begin{tabular}{|c|c|}\n"
        "\\hline\n"
        "$ & % \\\\\n"
        "_ & & \\\\\n"
        "\\hline\n"
        "\\end{tabular}"
    )
    assert generate_table(data) == expected_output
