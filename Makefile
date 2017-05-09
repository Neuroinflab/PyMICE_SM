
WEAVE=Pweave -f tex -F ${FIGDIR}
TANGLE=Ptangle
TOUCH=touch
RM=rm -rf
PDFLATEX=pdflatex
#PDFLATEX=pdflatex --shell-escape

FIGDIR=figures
EXAMPLES=example1.py example2.py example3.py example4.py get_example_data.py
TEX_DYNAMIC_ILLUSTRATED=example2.tex example3.tex example4.tex
TEX_DYNAMIC_NOT_ILLUSTRATED=get_example_data.tex example1.tex pymice_reproducibility.tex pymice_overview.tex
TEX_DYNAMIC=${TEX_DYNAMIC_ILLUSTRATED} ${TEX_DYNAMIC_NOT_ILLUSTRATED}
TEX_STATIC=example2_figure_caption.tex pymice_abstract.tex pymice_acknowledgements.tex pymice_discussion.tex pymice_examples.tex pymice_intellicage.tex pymice_introduction.tex pymice_technical.tex pymice_termsofuse.tex
DYNAMIC_FIGURES=${FIGDIR}/example2_Figure_1.pdf ${FIGDIR}/example3_Figure_1.pdf ${FIGDIR}/example4_Figure_1.pdf
STATIC_FIGURES=${FIGDIR}/apiScheme.pdf ${FIGDIR}/FigureIC.pdf
FIGURES=${DYNAMIC_FIGURES} ${STATIC_FIGURES}
TEX_SRC=${TEX_STATIC} ${TEX_DYNAMIC}
BIB_SRC=pymice.bib szymonall.bib
STYLES=spmpsci.bst svglov3.clo svjour3.cls
C57_AB=C57_AB C57_AB/2012-08-28\ 13.44.51.zip C57_AB/2012-08-28\ 15.33.58.zip C57_AB/2012-08-31\ 11.46.31.zip C57_AB/2012-08-31\ 11.58.22.zip C57_AB/timeline.ini
FVB=FVB FVB/2016-07-20\ 10.11.11.zip FVB/timeline.ini
DATA=${C57_AB} ${FVB} demo.zip
TEMPORARY_FILES=COPYING LICENSE example.eps article.aux article.bbl article.blg article.log article.out supplementary_reproducibility.tex supplementary_materials.aux supplementary_materials.bbl supplementary_materials.blg supplementary_materials.log supplementary_materials.out supplementary_materials.toc
MISSING_NP_DATA=2014-09-11\ 14.13.34.zip
SUPPLEMENTARY_MATERIALS=supplementary_materials.pdf article_source.zip ${EXAMPLES} ${DATA}

ALL=article.pdf supplementary_materials.zip

all: ${ALL}
.PHONY: all clean

clean:
	${RM} ${ALL} ${TEX_DYNAMIC} ${SUPPLEMENTARY_MATERIALS} ${DATA} ${DYNAMIC_FIGURES} ${TEMPORARY_FILES}

article.pdf: article.tex ${TEX_SRC} ${BIB_SRC} ${FIGURES} ${STYLES}
supplementary_materials.pdf: supplementary_materials.tex ${BIB_SRC} supplementary_reproducibility.tex ${STYLES}

article.pdf supplementary_materials.pdf:
	${PDFLATEX} $<
	bibtex $(basename $<)
	${PDFLATEX} $<
	${PDFLATEX} $<

example1.tex: demo.zip
example2.tex: ${FVB}
example3.tex example4.tex: ${C57_AB}
pymice_overview.tex: 2014-09-11\ 14.13.34.zip

example%.tex ${FIGDIR}/example%_Figure_1.pdf: example%.texw
	${WEAVE} $<

${TEX_DYNAMIC_NOT_ILLUSTRATED} supplementary_reproducibility.tex: %.tex: %.texw
	${WEAVE} $<

${EXAMPLES}: %.py: %.texw
	${TANGLE} $<

${DATA}: get_example_data.py
	python get_example_data.py
	${TOUCH} demo.zip ${C57_AB} ${FVB}

TEXW_SOURCES=$(TEX_DYNAMIC:%.tex=%.texw)
SOURCES=${MISSING_NP_DATA} Makefile article.tex ${TEX_STATIC} ${TEXW_SOURCES} ${BIB_SRC} ${STATIC_FIGURES} ${STYLES} supplementary_materials.tex supplementary_reproducibility.texw

article_source.zip: ${SOURCES}
	zip -9 $@ ${SOURCES}

supplementary_materials.zip: ${SUPPLEMENTARY_MATERIALS} ${MISSING_NP_DATA}
	zip -9 $@ ${SUPPLEMENTARY_MATERIALS} ${MISSING_NP_DATA}

