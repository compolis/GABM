# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# set of options see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
# Always prioritize the local src directory for imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
if src_path not in sys.path:
	sys.path.insert(0, src_path)

# -- Project information -----------------------------------------------------

project = 'GABM'
copyright = '2026, GABM contributors, University of Leeds'
author = 'Andy Turner'

# -- General configuration ---------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'myst_parser']
autosummary_generate = True

# Ensure full API details in autodoc
autodoc_default_options = {
	'members': True,
	'undoc-members': True,
	'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
