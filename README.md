# PyMICE – a Python library for analysis of IntelliCage data
## Source of the article
### Authors
* Jakub M. Dzik
* Alicja Puścian
* Zofia Mijakowska
* Kasia Radwanska
* Szymon Łęski


### Introduction
In order to meet the standarts of reproducibility and enable a reproducibility
review we decided to publish the data and complete source of the article.


### Requirements
We claim that all results presented in the article may be reproduced on a Linux
machine with an interpreter of Python programming language v. 2.7.3, PyMICE
v. 1.1.0, NumPy v. 1.6.1, matplitlib v. 1.1.1rc, dateutil v. 1.5 and pytz
v. 2012c.

We have not tested if the results are reproducible on other operating systems,
however it is likely.

To reproduce the article itself (generate a new PDF document based on the
reproduced results), pdflatex (v. 3.1415926), BibTeX (v. 0.99d), and Pweave
(v. 0.24) tools are necessary.


### Reproduction of the article

To automatically generate a custom version of the article based on reproduced
results rather than on the results claimed by the authors, perform the following
procedure: copy content of the repository to the working directory.

In case the GNU Make tool (or similar) is installed in the system, to reproduce
the article run:

```bash
$ make article.pdf
```

If GNU Make tool is not installed, you need to weave the texw files. It is
important to weave get\_example\_data.texw as the first file, since example
data are saved in the working directory during its weaving.

```bash
$ Pweave -f tex get\_example\_data.texw
$ Pweave -f tex pymice\_overview.texw
$ Pweave -f tex pymice\_reproducibility.texw
$ Pweave -f tex example1.texw
$ Pweave -f tex -F figures example2.texw
$ Pweave -f tex -F figures example3.texw
$ Pweave -f tex -F figures example4.texw
```

After all files have been weaved, compile the LaTeX source.

```bash
$ pdflatex article.tex
$ bibtex article
$ pdflatex article.tex
$ pdflatex article.tex
```

The article.pdf file contains the reproduced article.


### Reproduction of the supplementary materials

To automatically generate a custom version of the supplementary materials
perform the following procedure: copy content of the repository to the working
directory.

In case the GNU Make tool (or similar) is installed in the system, to reproduce
the supplementary materials run:

```bash
$ make supplementary\_materials.zip
```

The archive **supplementary\_materials.zip** contains the complete supplementary
materials.

If GNU Make tool is not installed, you need to generate the supplementary
materials manually.

First tangle and execute script providing the raw data.

```bash
$ Ptangle get\_example\_data.texw
$ python get\_example\_data.py
```

Tangle the examples.

```bash
$ Ptangle example1.texw
$ Ptangle example2.texw
$ Ptangle example3.texw
$ Ptangle example4.texw
```

Weave the reproducibility statement.

```bash
$ Pweave -f tex supplementary\_reproducibility.texw
```

Eventually compile the LaTeX source.

```bash
$ pdflatex supplementary\_materials.tex
$ bibtex supplementary\_materials
$ pdflatex supplementary\_materials.tex
$ pdflatex supplementary\_materials.tex
```

The **supplementary\_materials.pdf** file contains description of supplementary
materials.


### Acknowledgements

> JD, KR and SŁ supported by a Symfonia NCN grant UMO-2013/
> 08/W/NZ4/00691. AP supported by a grant from Switzerland through the Swiss
> Contribution to the enlarged European Union (PSPB-210/2010 to Ewelina Knapska
> and Hans-Peter Lipp).
> 
> KR and ZM supported by an FNP grant POMOST/2011-4/7 to KR.
