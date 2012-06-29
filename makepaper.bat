#!/bin/csh

rm -f *.log *.out *.aux *.dvi *~ *.bbl *.blg
rm -f ms.ps ms.pdf

ls -l

latex ms
bibtex ms
latex ms
latex ms
latex ms
dvips -o ms.ps ms.dvi
dvipdf ms

if( $1 == "o" ) open ms.pdf
# the end
