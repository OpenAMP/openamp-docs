# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Work flow context -------------------------------------------------------
import os

pwd = os.getcwd()
url_base = os.environ.get('READTHEDOCS_CANONICAL_URL', "file:" + pwd + "/_build/html/")
if not url_base.endswith("/"):
    url_base = url_base + "/"

version = os.environ.get('READTHEDOCS_VERSION', "latest")
is_release = version.startswith(("v", "V"))
is_pr = not is_release and version != "latest"
latest_url = "https://openamp.readthedocs.io/en/latest/"

#print(f"url_base: {url_base}  version: {version}  is_release: {is_release}  is_pr: {is_pr}")

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'OpenAMP'
copyright = '2023, OpenAMP Project'
author = 'OpenAMP Project'

# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinxcontrib.jquery",
    'sphinx.ext.autosectionlabel',
    'sphinxcontrib.plantuml',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'sphinx.ext.todo',
    'rst2pdf.pdfbuilder',
    'myst_parser',
]

pdf_documents = [('index', u'openamppdf', u'Sample openamppdf doc', u'Tammy Leino'),]

#plantuml = '/usr/bin/plantuml -Djava.awt.headless=true -config uml/plantuml.cfg '

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.git']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_style = 'css/mystyle.css'

# below copied / hacked from Zephyr projects' zephyr/doc/conf.py
docs_title = "Docs / {}".format(version if is_release else "Latest")
html_context = {
    "show_license": True,
    "docs_title": docs_title,
    "is_release": is_release,
    "is_pr": is_pr,
    "current_version": version,
    "html_base": url_base,
    "latest_url": latest_url,
    "display_vcs_link": False,
    "reference_links": {
        "open-amp API": f"{url_base}doxygen/openamp/index.html",
        "libmetal API": f"{url_base}doxygen/libmetal/index.html",
        "System Devicetree Spec": f"{url_base}lopper/specification/source/index.html",
    }
}

print(f"url_base: {url_base}  version: {version}  is_release: {is_release}  is_pr: {is_pr}")
print(f"html_context: {html_context}")
