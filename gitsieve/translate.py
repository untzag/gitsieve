"""Translate a shell PATTERN to a regular expression."""


# --- import --------------------------------------------------------------------------------------


import re


# --- objects -------------------------------------------------------------------------------------


__all__ = ['translate']


# --- functions -----------------------------------------------------------------------------------


def _translate_segment(segment):
    # adapted from https://github.com/jelmer/dulwich/blob/master/dulwich/ignore.py
    if segment == "*":
        return '[^/]+'
    res = ""
    i, n = 0, len(segment)
    while i < n:
        c = segment[i:i+1]
        i = i+1
        if c == '*':
            res += '[^/]*'
        elif c == '?':
            res += '.'
        elif c == '[':
            j = i
            if j < n and segment[j:j+1] == '!':
                j = j+1
            if j < n and segment[j:j+1] == ']':
                j = j+1
            while j < n and segment[j:j+1] != ']':
                j = j+1
            if j >= n:
                res += '\\['
            else:
                stuff = segment[i:j].replace('\\', '\\\\')
                i = j+1
                if stuff.startswith('!'):
                    stuff = '^' + stuff[1:]
                elif stuff.startswith('^'):
                    stuff = '\\' + stuff
                res += '[' + stuff + ']'
        else:
            res += re.escape(c)
    return res


def translate(pat):
    # adapted from https://github.com/jelmer/dulwich/blob/master/dulwich/ignore.py
    res = '(?ms)'
    if '/' not in pat[:-1]:
        # If there's no slash, this is a filename-based match
        res += '(.*/)?'
    if pat.startswith('**/'):
        # Leading **/
        pat = pat[2:]
        res += '(.*/)?'
    if pat.startswith('/'):
        pat = pat[1:]
    for i, segment in enumerate(pat.split('/')):
        if segment == '**':
            res += '(/.*)?'
            continue
        else:
            res += ((re.escape('/') if i > 0 else '') + _translate_segment(segment))
    if not pat.endswith('/'):
        res += '/?'
    return res + '\Z'