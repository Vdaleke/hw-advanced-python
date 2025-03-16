from advanced_python_hw2_vdaleke import (generate_image,  # type: ignore
                                         generate_table)

if __name__ == "__main__":
    example_data = [
        ["Страна", "Столица", "Население (млн)"],
        ["Россия", "Москва", 146],
        ["Франция", "Париж", 68],
        ["Германия", "Берлин", 83],
        ["Япония", "Токио", 125],
    ]

    tex_table = generate_table(example_data)

    image_path = "photo_2025-03-16_21-45-04.jpg"
    tex_image = generate_image(
        image_path,
        width="0.5\\textwidth",
        caption="Example Image",
        label="fig:example_image",
    )

    latex_document = (
        r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{graphicx}
\begin{document}

"""
        + tex_table
        + "\n"
        + tex_image
        + "\n\\end{document}"
    )

    with open("latex/document.tex", "w", encoding="utf-8") as f:
        f.write(latex_document)
