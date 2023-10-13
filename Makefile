# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
READTHEDOCS_VERSION_NAME ?= "desk check"
SOURCEDIR     = .
BUILDDIR      = _build

#IMG_SRC_DIR = uml
#IMG_TGTS = $(patsubst %.txt,%.eps,$(wildcard $(IMG_SRC_DIR)/*.txt))

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help clean doxygen doxygen_libmetal doxygen_openamp doxygen_copy

.NOTPARALLEL:

#%.txt:;

#%.eps: %.txt
	#plantuml -config uml/plantuml.cfg -o ../_build/html/uml/ uml/*.txt

#images: ${IMG_TGTS};

doxygen: doxygen_libmetal doxygen_openamp

doxygen_libmetal:
	cmake -B${BUILDDIR}/libmetal -DVERSION_NAME=${READTHEDOCS_VERSION_NAME} \
           -DWITH_DOC=true libmetal
	make -C ${BUILDDIR}/libmetal doc

doxygen_openamp:
	cmake -B${BUILDDIR}/openamp -DVERSION_NAME=${READTHEDOCS_VERSION_NAME} \
           -DWITH_LIBMETAL_FIND=false -DWITH_DOC=true open-amp
	make -C ${BUILDDIR}/openamp doc

# using hard coded name here to avoid bad things if BUILDDIR is ever empty or /
clean:
	rm -rf _build/*

html: doxygen html-fast doxygen_copy
	@echo Done with full html target

doxygen_copy:
	rm -rf   ${BUILDDIR}/doxygen || true
	mkdir -p ${BUILDDIR}/html/doxygen/libmetal
	mkdir -p ${BUILDDIR}/html/doxygen/openamp
	cp -a    ${BUILDDIR}/libmetal/doc/html/* ${BUILDDIR}/html/doxygen/libmetal/
	cp -a    ${BUILDDIR}/openamp/doc/html/*  ${BUILDDIR}/html/doxygen/openamp/

html-fast:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: #images
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
