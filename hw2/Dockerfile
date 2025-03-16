FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    texlive-latex-base texlive-fonts-recommended texlive-lang-cyrillic \
    texlive-extra-utils texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY generate-latex ./generate-latex

WORKDIR /app/generate-latex
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --only main

CMD ["sh", "-c", "python generate_latex.py && cd latex && pdflatex -interaction=nonstopmode document.tex"]
