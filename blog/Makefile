%.pdf: %.md main.bib
	pandoc --pdf-engine=xelatex -f markdown+inline_notes+citations -t latex -C -o $@ $<
%.html: %.md main.bib
	pandoc -f markdown+inline_notes  -t html --highlight-style zenburn --mathjax --standalone -o $@ $<
