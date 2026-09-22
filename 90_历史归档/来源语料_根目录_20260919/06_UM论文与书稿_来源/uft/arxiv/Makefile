.PHONY: all pdf clean submit

TEX = main
BIB = references

all: pdf

pdf:
	@echo "Building PDF..."
	@pdflatex -interaction=nonstopmode $(TEX).tex
	@bibtex $(TEX)
	@pdflatex -interaction=nonstopmode $(TEX).tex
	@pdflatex -interaction=nonstopmode $(TEX).tex
	@echo "Done: $(TEX).pdf"

clean:
	rm -f $(TEX).{aux,bbl,blg,log,out,pdf,synctex.gz,toc,fdb_latexmk,fls}

submit: pdf
	@echo "Ready for arXiv submission. Upload: $(TEX).tar.gz"
	tar -czvf $(TEX).tar.gz $(TEX).tex $(BIB).bib figures/
	@echo "Submit $(TEX).tar.gz to arXiv.org"

# If using XeLaTeX (for Unicode support)
xepdf:
	xelatex -interaction=nonstopmode $(TEX).tex
	bibtex $(TEX)
	xelatex -interaction=nonstopmode $(TEX).tex
	xelatex -interaction=nonstopmode $(TEX).tex
