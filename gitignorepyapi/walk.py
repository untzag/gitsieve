"""Walk a repository while ignoring files."""


# --- import --------------------------------------------------------------------------------------


import os

from .repository import Repository

# --- objects -------------------------------------------------------------------------------------


__all__ = ['walk']


# --- functions -----------------------------------------------------------------------------------


def walk(repository, ignore_file_pattern='*.gitignore'):
    """Walk a repository, ignoring files.
    
    Parameters
    ----------
    
    """
    r = Repository(path=repository, ignore_file_pattern=ignore_file_pattern)
    for root, dirs, files in os.walk(repository):
        if r.is_ignored(root):
            continue
        dirs = [d for d in dirs if not r.is_ignored(os.path.join(root, d))]
        files = [f for f in files if not r.is_ignored(os.path.join(root, f))]
        yield root, dirs, files