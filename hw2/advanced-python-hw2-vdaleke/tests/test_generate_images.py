import pytest

from advanced_python_hw2_vdaleke import generate_image


def test_generate_image_defaults():
    image_path = "path/to/image.png"
    expected_output = (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width=\\textwidth]{{{image_path}}}\n"
        "\\end{figure}"
    )
    assert generate_image(image_path) == expected_output


def test_generate_image_with_caption():
    image_path = "path/to/image.png"
    caption = "This is a sample image."
    expected_output = (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width=\\textwidth]{{{image_path}}}\n"
        f"\\caption{{{caption}}}\n"
        "\\end{figure}"
    )
    assert generate_image(image_path, caption=caption) == expected_output


def test_generate_image_with_label():
    image_path = "path/to/image.png"
    label = "fig:sample_image"
    expected_output = (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width=\\textwidth]{{{image_path}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}"
    )
    assert generate_image(image_path, label=label) == expected_output


def test_generate_image_with_caption_and_label():
    image_path = "path/to/image.png"
    caption = "This is a sample image."
    label = "fig:sample_image"
    expected_output = (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width=\\textwidth]{{{image_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}"
    )
    assert generate_image(image_path, caption=caption, label=label) == expected_output


def test_generate_image_with_custom_width():
    image_path = "path/to/image.png"
    width = "0.5\\textwidth"
    expected_output = (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width={width}]{{{image_path}}}\n"
        "\\end{figure}"
    )
    assert generate_image(image_path, width=width) == expected_output
