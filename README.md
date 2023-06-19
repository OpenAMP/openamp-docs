# openamp_docs
OpenAMP Documentation sources for Sphinx

If you are looking for the end-user version of the documentation, you can find [the OpenAMP Readthedocs site here](https://openamp.readthedocs.io/en/latest/index.html "OpenAMP Readthedocs site").

## online review

Creating a PR for openamp/openamp-docs will build the new docs and they can
be reviewed in the PR.

## desktop review

If you wish to build the documents on the desktop, you can do as follows.

Setup for Ubuntu 22.04:

    $ sudo apt update
    $ sudo apt install cmake doxygen libhugetlbfs-dev libsysfs-dev
    $ sudo apt install python3-pip git
    $ git clone --recurse https://github.com/openAMP/openamp-docs.git
    $ cd openamp-docs
    $ python3 -m pip install -r requirements.txt

To build and view the html documents:

    $ make html
    $ xdg-open _build/html/index.html

To build and view the pdf:

    $ make pdf
    $ xdg-open _build/pdf/openamppdf.pdf

Notes:
* The build process currently produces many warnings
* The doxygen content is not included in the pdf
* The doxygen content is not styled like the rest of the html documents
* The doxygen context does not integrate into the menu structure; use the browser back button to get back.
