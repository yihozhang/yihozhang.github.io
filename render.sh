#!/bin/bash

for f in blog/*.md; do
    echo "Rendering $f"
    pandoc --pdf-engine=xelatex -f markdown+inline_notes -t latex -o "${f%.md}.pdf" "$f"
    pandoc -f markdown+inline_notes -t html --highlight-style zenburn --mathjax --standalone -o "${f%.md}.html" "$f"
done