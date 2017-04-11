from . import beacon, csv, ntriples, jskos
from .base import LinkReader, LinkWriter, DeltaWriter

import os

formats = {f.name: f for f in [csv, beacon, ntriples, jskos]}

readers = {f: formats[f].Reader for f in formats if hasattr(formats[f],'Reader')}
writers = {f: formats[f].Writer for f in formats if hasattr(formats[f],'Writer')}


def guessFormat(filename, names):
    name, ext = os.path.splitext(filename)
    try:
        return [formats[n].name for n in names if formats[n].extension == ext][0]
    except IndexError:
        pass

__all__ = ['readers', 'writers', 'guessFormat', 'LinkReader', 'LinkWriter', 'DeltaWriter']
