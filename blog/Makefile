%.pdf: %.md
	pandoc --pdf-engine=xelatex -f markdown+inline_notes -t latex -o $@ $<
%.html: %.md
	pandoc -f markdown+inline_notes  -t html --highlight-style zenburn --mathjax --standalone -o $@ $<
