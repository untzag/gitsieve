"""Ignore file object and parts thereof."""


# --- import --------------------------------------------------------------------------------------


import os
import re

from .translate import translate


# --- objects -------------------------------------------------------------------------------------


__all__ = ['File']


# --- functions -----------------------------------------------------------------------------------


def read(f):
    for l in f:
        l = l.rstrip('\r\n')
        # ignore blank lines
        if not l:
            continue
        # ignore comments
        if l.startswith('#'):
            continue
        # ignore trailing spaces, unless they are quoted with a backslash.
        while l.endswith(' ') and not l.endswith('\\ '):
            l = l[:-1]
        l = l.replace('\\ ', ' ')
        yield l


# --- classes -------------------------------------------------------------------------------------


class Pattern(object):

    def __init__(self, pattern):
        self.pattern = pattern
        if pattern[0:1] == '!':
            self.is_exclude = False
            pattern = pattern[1:]
        else:
            if pattern[0:1] == '\\':
                pattern = pattern[1:]
            self.is_exclude = True
        self._re = re.compile(translate(pattern))

    def __repr__(self):
        return 'gitsieve.file.Pattern object \'{0}\' at {1}'.format(self.pattern, id(self))

    def match(self, path):
        return bool(self._re.search(path))


class File(object):

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.patterns = []
        with open(path) as f:
            for l in read(f):
                self.patterns.append(Pattern(l))
