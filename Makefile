NAME=ms
SECTIONS=app-chemistry.tex app-datastruct.tex app-gravity.tex app-IO.tex \
	app-ppmhydro.tex app-zeushydro.tex code-tests.tex conclusions.tex \
	development.tex discussion.tex introduction.tex local-commands.tex \
	numerical-amr.tex numerical-analysis.tex numerical-chemistry.tex \
	numerical-cooling.tex numerical-gravity.tex \
        numerical-mhd-ct.tex \
	numerical-muscl.tex numerical-overview.tex numerical-particle.tex \
	numerical-ppm.tex numerical-radiation-fld.tex \
	numerical-radiation-homogeneous.tex numerical-radiation-raytracing.tex \
	numerical-starformation.tex numerical-timestep.tex numerical-zeus.tex \
	overview.tex parallel.tex summary.tex
LATEX=latex -interaction=nonstopmode

all:  $(NAME).pdf

dvi: $(NAME).tex $(SECTIONS)
	$(LATEX) $(NAME) || true
	bibtex $(NAME)
	$(LATEX) $(NAME) || true 
	bibtex $(NAME)
	$(LATEX) $(NAME) || true 
	$(LATEX) $(NAME)

$(NAME).pdf: $(NAME).tex $(SECTIONS)
	$(LATEX) $(NAME) || true
	bibtex $(NAME)
	$(LATEX) $(NAME) || true 
	bibtex $(NAME)
	$(LATEX) $(NAME) || true 
	$(LATEX) $(NAME) || true 
	dvipdf $(NAME).dvi $(NAME).pdf
	rm -f $(NAME).blg $(NAME).log $(NAME).aux

clean:
	rm -f *~ *.aux *.dvi *.gz *.out *.toc *log *-temp.* *.blg *~ $(NAME).ps $(NAME).bbl $(NAME).pdf


