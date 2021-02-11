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
    'sphinx.ext.napoleon',
    'matplotlib.sphinxext.plot_directive',    
    'numpydoc',  # handle NumPy documentation formatted docstrings]
    'nbsphinx',
<<<<<<< HEAD
]

#napoleon_numpy_docstring = True

=======
    #'guzzle_sphinx_theme',
]

napoleon_numpy_docstring = True
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
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

#autosummary_generate = True
master_doc = 'index'

# matplotlib plot directive
plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
<<<<<<< HEAD
# Required theme setup
html_theme = 'sphinx_material'

# Set link name generated in the top bar.
html_title = 'HotStepper'

=======
html_theme = 'sphinx_material'
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
# Material theme options (see theme.conf for more information)
html_theme_options = {

    # Set the name of the project to appear in the navigation.
    'nav_title': 'HotStepper',

    # Set you GA account ID to enable tracking
    #'google_analytics_account': 'UA-XXXXX',

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    'base_url': 'https://github.com/TangleSpace/HotStepper',

    # Set the color and the accent color
<<<<<<< HEAD
    'color_primary': 'indigo',
    'color_accent': 'deep-purple',
=======
    'color_primary': 'Indigo',
    'color_accent': 'light-indigo',
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/TangleSpace/HotStepper',
    'repo_name': 'HotStepper',

    # Visible levels of the global TOC; -1 means unlimited
<<<<<<< HEAD
    'globaltoc_depth': 2,
=======
    'globaltoc_depth': 3,
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
    # If False, expand all TOC entries
    'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
}

# html_theme_options = {
#     "google_analytics_account": "UA-65430466-2",
#     "base_url": "https://railing.readthedocs.io/en/latest/",
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