# -*- coding: utf-8 -*-
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
import os
import sys
import glob
import shutil
import urllib

autodoc_mock_imports = ["openvino", "pytorch_lightning", "keras"]

# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, '.')
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath("../../../python/friesian/src/"))
sys.path.insert(0, os.path.abspath("../../../python/chronos/src/"))
sys.path.insert(0, os.path.abspath("../../../python/dllib/src/"))
sys.path.insert(0, os.path.abspath("../../../python/orca/src/"))
sys.path.insert(0, os.path.abspath("../../../python/serving/src/"))
sys.path.insert(0, os.path.abspath("../../../python/nano/src/"))



# -- Project information -----------------------------------------------------
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
#html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/intel-analytics/BigDL",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "path_to_docs": "doc/source",
    "home_page_in_toc": True,
}

# The suffix of source filenames.
from recommonmark.parser import CommonMarkParser
source_suffix = {'.rst': 'restructuredtext',
                 '.txt': 'markdown',
                 '.md': 'markdown',}

master_doc = 'index'

project = 'BigDL'
copyright = '2020, BigDL Authors'
author = 'BigDL Authors'

# The short X.Y version
#version = ''
# The full version, including alpha/beta/rc tags
#from zoo import __version__ as version
#release = version


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#extensions = [
 #   'sphinx.ext.autodoc',
#]
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx_click.ext',
    'sphinx-jsonschema',
    'sphinx.ext.napoleon',
    'sphinxemoji.sphinxemoji',
    'sphinx_copybutton',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosectionlabel',
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinx_tabs.tabs',
    'sphinx_design',
    'sphinx_external_toc',
    'sphinx_design',
    'nbsphinx'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.

#exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

exclude_patterns = ['_build']
#todo_include_todos = False


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document namesan
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'BigDL Documentation'



# -- Options for external TOC tree ---
external_toc_exclude_missing = False
external_toc_path = "_toc.yml"

# this is to surpresswarnings about explicit "toctree" directives
suppress_warnings = ["etoc.toctree"]

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'bigdl.tex', 'bigdl Documentation',
     'bigdl', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'bigdl', 'bigdl Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'bigdl', 'bigdl Documentation',
     author, 'bigdl', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

autoclass_content = 'both'
autodoc_member_order = 'bysource'

# app setup hook for AutoStructify
from recommonmark.transform import AutoStructify
def setup(app):
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
        'enable_math': False,
        'enable_inline_math': False,
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
    }, True)
    app.add_transform(AutoStructify)

# disable notebook execution
nbsphinx_execute = 'never'