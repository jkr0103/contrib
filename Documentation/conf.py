# pylint: skip-file
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import collections
import pathlib
import subprocess

# -- Project information -----------------------------------------------------

project = 'Gramine External Contributions'
copyright = '2021, Gramine Contributors'
author = 'Gramine Contributors'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'breathe',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
}

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

highlight_language = 'c'
primary_domain = 'c'

rst_prolog = '''
.. |~| unicode:: 0xa0
   :trim:
'''

breathe_projects = {
    'gramine-contrib': '_build/doxygen/xml',
}

def generate_doxygen(app):
    subprocess.check_call(['doxygen', 'Doxyfile'])

def setup(app):
    app.add_stylesheet('css/gramine.css')
    app.connect('builder-inited', generate_doxygen)

breathe_domain_by_extension = {
    'h': 'c',
}

todo_include_todos = True

nitpicky = True
nitpick_ignore = [
    ('c:type', 'bool'),
    ('c:type', 'toml_table_t'),
    ('c:type', 'uint32_t'),
    ('c:type', 'uint64_t'),
    ('c:type', 'union'),
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
}
html_logo = 'gramine_logo.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
#    ('manpages/is_sgx_available', 'is_sgx_available', 'Check SGX compatibility', [author], 1),
]

# barf if a page is not included
assert (collections.Counter(str(p.with_suffix(''))
        for p in pathlib.Path().glob('manpages/*.rst')
        if not p.stem == 'index')
    == collections.Counter(source
        for source, *_ in man_pages))
