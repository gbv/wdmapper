# -*- coding: utf-8 -*-
"""
Input and output formats to read and write mappings.

Usage:

    name = wdmapper.format.guessFormat(filename)

    reader = wdmapper.format.readers[name](stream)
    reader.start()
    for link in reader.next():
        ...

    writer = wdmapper.format.writers[name](stream)
    writer.start()
    writer.write_link(link)
    writer.write_delta(delta)

"""

from . import beacon, csv, ntriples, jskos, quicks, markdown

import os

formats = {f.name: f for f in [csv, beacon, ntriples, jskos, quicks, markdown]}

readers = {f: formats[f].Reader for f in formats if hasattr(formats[f],'Reader')}
writers = {f: formats[f].Writer for f in formats if hasattr(formats[f],'Writer')}


def guessFormat(filename, names=formats.keys()):
    """Guess a reader/writer format from given filename and possible format names."""
    name, ext = os.path.splitext(filename)
    try:
        for name in names:
            if name in formats and hasattr(formats[name],'extension'):
                if formats[name].extension == ext:
                    return name
    except IndexError:
        pass

__all__ = [
    'readers',
    'writers',
    'guessFormat'
]
