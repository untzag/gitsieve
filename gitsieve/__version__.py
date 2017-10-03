"""gitsieve version."""


# --- import --------------------------------------------------------------------------------------


import os


# --- objects -------------------------------------------------------------------------------------


here = os.path.abspath(os.path.dirname(__file__))

__all__ = ['__version__']


# --- workspace -----------------------------------------------------------------------------------


with open(os.path.join(os.path.dirname(here), 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

