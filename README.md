# openamp_docs
OpenAMP Documentation sources for Sphinx

If you are looking for the end-user version of the documentation, you can
find [the OpenAMP Readthedocs site here](https://openamp.readthedocs.io/en/latest/index.html "OpenAMP Readthedocs site").

## How to Contribute

The OpenAMP Documentation is an open source project and welcomes community contributions.

We use standard Github mechanism for a pull request (PR). Please refer to github documentation
for help.

We recommend you verify your changes locally using the
[Desktop Build and Review](#desktop-build-and-review) before submitting
for an [Online Pull Request and Review](#online-pull-request-and-review)

## Documentation Guidelines

The following are guidelines to follow as part of your contribution.

* Documentation should use Restructured Text files ending in .rst for consumption by
  [Sphinx](https://www.sphinx-doc.org/en/master/index.html)
* Maintain a document source line length of 100 characters when possible
* For cross-references to documentation in source code submodules use
  [auto-generated anchors](#cross-referencing-to-markdown-files)
* To link to source code you should use
  [embedded doxygen content or a hyperlink](#linking-to-source-code)
* For tables use
  * [Grid Tables](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#grid-tables)
  when possible, for clearer reading in the document source or
  * [CSV Tables](https://docutils.sourceforge.io/docs/ref/rst/directives.html#csv-table)

## Online Pull Request and Review

Creating a PR for openamp/openamp-docs will build the new docs and they can be reviewed in the PR.

You can locate the Sphinx rendered documentation for the PR by
* Opening the pull request in
  [Github OpenAMP Pull Requests](https://github.com/OpenAMP/openamp-docs/pulls)
* Clicking the down arrow next to the **All checks have passed** at the
  bottom of the PR
* Clicking on the link to **docs/readthedocs.org:openamp**

## Desktop Build and Review

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
* The doxygen context does not integrate into the menu structure; use the browser back button
to get back.

## Cross-Referencing to Markdown files

When making a cross-reference from a Restructured text (rst) file to a Markdown file (md),
usually in a source code repository like open-amp or libmetal, you should do so by leveraging the
[auto-generated header anchors](https://myst-parser.readthedocs.io/en/stable/syntax/optional.html#syntax-header-anchors).

For example this example is a reference to a markdown file within the git submodule lopper's
README-architecture.md file section 'Lopper Processing Flow'

```
:ref:`Lopper Architecture Readme<lopper/README-architecture:lopper processing flow:>`
```

This will ensure that references are to the version of git submodule being described by the
documentation.

## Linking to Source Code

When cross-referencing to source code there are two methods you can use.
You can embed the source code 'item', be it a struct or function etc, within  your documentation,
or provide a link to within the full doxygen generated  documentation.

### Embedding Source Code Documentation

Embedding doxygen generated documentation from the source code repository is achieved using the
[Breathe Sphinx extension](https://breathe.readthedocs.io).

The following are examples of embedding the doxygen content. Two projects are defined for the
open-amp and libmetal repositories, named openamp_doc_embed and libmetal_doc_embed respectively.

* libmetal function "metal_allocate_memory"

```
.. doxygenfunction:: metal_allocate_memory
   :project: libmetal_doc_embed
```

* open-amp type definition "rpmsg_ns_unbind_cb"

```
.. doxygentypedef:: rpmsg_ns_unbind_cb
   :project: openamp_doc_embed
```

* open-amp structure "remoteproc_virtio", including the members of the struct

```
.. doxygenstruct:: remoteproc_virtio
   :members:
```

Note on the last example the project is not named, so the default openamp_doc_embed project
is used.

### Linking to Source Code Documentation

It is also possible to create a hyperlink to the doxygen generated documentation of the source.
This is achieved using the [Doxylink extension](https://sphinxcontrib-doxylink.readthedocs.io).

The following are examples of creating hyperlinks to the doxygen generated documentation.

* open-amp rpmsg_device structure
```
:openamp_doc_link:`rpmsg_device <rpmsg_device>`
```

* libmetal metal_sys_init function
```
:libmetal_doc_link:`metal_sys_init <metal_sys_init>`
```
