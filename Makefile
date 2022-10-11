# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

#IMG_SRC_DIR = uml
#IMG_TGTS = $(patsubst %.txt,%.eps,$(wildcard $(IMG_SRC_DIR)/*.txt))

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

#%.txt:;

#%.eps: %.txt
	#plantuml -config uml/plantuml.cfg -o ../_build/html/uml/ uml/*.txt

#images: ${IMG_TGTS};

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile #images
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
