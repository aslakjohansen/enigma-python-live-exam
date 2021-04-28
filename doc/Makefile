TARGETS = \
	Enigma\ -\ Python\ Refresh\ Handouts.pdf \
	Enigma\ -\ Python\ Refresh\ Presentation.pdf \



all: ${TARGETS}

clean:
	rm -f ${TARGETS}

mrproper: clean
	touch d.aux d.log d~ d.nav d.out d.snm d.toc includes.d
	rm -f *.aux *.log *~ *.nav *.out *.snm *.toc includes.*



includes:
	rm -Rf includes
	mkdir includes

includes.python.timestamp: includes python_*.tex shared.tex
	cd .. ; bin/generate-tex-includes PDF doc/python_handouts.tex doc
	touch includes.python.timestamp



Enigma\ -\ Python\ Refresh\ Handouts.pdf: python_*.tex shared.tex includes.python.timestamp
	pdflatex -shell-escape python_handouts.tex
	pdflatex -shell-escape python_handouts.tex
	mv python_handouts.pdf Enigma\ -\ Python\ Refresh\ Handouts.pdf

Enigma\ -\ Python\ Refresh\ Presentation.pdf: python_*.tex shared.tex includes.python.timestamp
	pdflatex -shell-escape python_presentation.tex
	pdflatex -shell-escape python_presentation.tex
	mv python_presentation.pdf Enigma\ -\ Python\ Refresh\ Presentation.pdf


SDU\ DM\ -\ RDF\ Exercises.pdf: rdf_exercise_simpsons.tex
	pdflatex -shell-escape rdf_exercise_simpsons.tex
	pdflatex -shell-escape rdf_exercise_simpsons.tex
	mv rdf_exercise_simpsons.pdf SDU\ DM\ -\ RDF\ Exercises.pdf

