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
# sys.path.insert(0, os.path.abspath('.'))

import subprocess
process = subprocess.Popen(['./build.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait() # Wait for process to complete.

# iterate on the stdout line by line
for line in process.stdout.readlines():
    print(line)

import geocat.f2py

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


class Mock(MagicMock):

    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


MOCK_MODULES = ["xarray", "dask", "dask.array", "dask.array.core"]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx', 'sphinx.ext.mathjax'
]

napoleon_use_admonition_for_examples = True
napoleon_include_special_with_doc = True

autosummary_generate = True

# The master toctree document.
master_doc = 'index'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Project information -----------------------------------------------------

project = 'GeoCAT-f2py'

import datetime

current_year = datetime.datetime.now().year
copyright = u'{}, University Corporation for Atmospheric Research'.format(
    current_year)
author = u'GeoCAT'

# The version info for the project being documented
def read_version():
    for line in open('../meta.yaml').readlines():
        index = line.find('version')
        if index > -1:
            return line[index + 8:].replace('\'', '').strip()

# The short X.Y version.
version = read_version()

# The full version, including alpha/beta/rc tags.
release = read_version()


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

#html_theme = 'alabaster'
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    html_theme = 'default'
else:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/images/nsf.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']