"""Repository class."""


# --- import ---------------------=----------------------------------------------------------------


import os
import fnmatch

from .file import read, Pattern, File


# --- objects -------------------------------------------------------------------------------------


__all__ = ['Repository']


# --- classes -------------------------------------------------------------------------------------


class Repository(object):

    def __init__(self, path, ignore_file_pattern='*.gitignore'):
        self.path = os.path.abspath(path)
        self.ignore_file_pattern = ignore_file_pattern
        self.ignore_files = {}

    def _find_ignore_files(self, directory):
        directory = os.path.abspath(os.path.normpath(directory))
        while True:
            for p in os.listdir(directory):
                if fnmatch.fnmatch(p, self.ignore_file_pattern):
                    p = os.path.join(directory, p)
                    if p not in self.ignore_files.keys():
                        self.ignore_files[p] = File(p)
            if directory == self.path:
                break
            else:
                directory = os.path.dirname(directory)

    def is_ignored(self, path):
        path = os.path.abspath(path)
        ignored = False
        # TODO: consider removing hardcoded .git ignore
        if '.git' in path.split(os.path.sep):
            return True
        # collect applicable ignore_files
        if os.path.isdir(path):
            directory = path
        elif os.path.isfile(path):
            directory = os.path.dirname(path)
        else:
            # TODO: a good exception...
            raise Exception
        self._find_ignore_files(directory)
        # look for conditions
        for ignore_file in self.ignore_files.values():
            if not os.path.dirname(ignore_file.path) in path:
                continue
            relative_path = os.path.relpath(path, os.path.dirname(ignore_file.path))
            split_path = relative_path.split(os.sep)
            for pattern in ignore_file.patterns:
                for i in range(1, len(split_path)+1):
                    p = os.sep.join(split_path[0:i])
                    if os.path.isdir(os.path.join(self.path, p)):
                        p += '/'
                    if pattern.match(p):
                        if not pattern.is_exclude:
                            # if explicitly excluded, we can return right away
                            return False
                        else:
                            # must read the rest of the patterns looking for exclusion
                            # for now, store that a ignore match has occured
                            ignored = True
        return ignored
