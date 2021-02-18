# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..//'))
sys.path.insert(0, os.path.abspath('..'))
import hotstepper as hs


# -- Project information -----------------------------------------------------

project = hs.__packagename__
copyright = '2020, Jackson Storm'
author = hs.__author__
release = hs.__version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary', 
    'sphinx.ext.coverage', 
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.napoleon',
    'matplotlib.sphinxext.plot_directive',    
    'numpydoc',  # handle NumPy documentation formatted docstrings]
    'nbsphinx',
]

#napoleon_numpy_docstring = True

source_suffix = ['.rst', '.ipynb']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store',
    'examples/.ipynb_checkpoints',
    'articles/.ipynb_checkpoints',
    'examples/Index.ipynb'
]

napoleon_numpy_docstring = True
napoleon_google_docstring = False
#napoleon_use_param = False
#napoleon_use_ivar = True

#autosummary_generate = True
master_doc = 'index'

# matplotlib plot directive
#plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False

# autodoc_default_options = {
#     'members': True,
#     #'show-inheritance': True,
# }
## Generate autodoc stubs with summaries from code
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
html_title = 'HotStepper'
html_theme = 'sphinx_material'

html_theme_options = {

    # Set the name of the project to appear in the navigation.
    'nav_title': 'HotStepper',

    # Set the color and the accent color
    'color_primary': 'indigo',
    'color_accent': 'deep-purple',


    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 3,
    # If False, expand all TOC entries
    'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
}

#html_theme = "sphinxawesome_theme"

# html_theme_options = {
#     'color': '#9c00ff'
# }

html_logo = 'images/HotstepperLogo.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# def setup(app):
#     app.add_css_file('custom.css')

# html_sidebars = {
#     "**":["logo.html", "globaltoc.html", "relations.html", "searchbox.html", "gumroad.html",]
# }