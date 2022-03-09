#!/bin/bash

for f in blog/*.md; do
    echo "Rendering $f"
    pandoc -f markdown -t pdf -o "${f%.md}.pdf" "$f"
    pandoc -f markdown -t html --mathjax --standalone -o "${f%.md}.html" "$f"
done