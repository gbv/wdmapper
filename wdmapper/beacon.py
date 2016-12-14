# -*- coding: utf-8 -*-
"""BEACON format writer."""

from __future__ import unicode_literals

# TODO: TIMESTAMP, CREATOR, HOMEPAGE
beacon_header = """\
#NAME:        {target[label]}
#DESCRIPTION: Mapping from {source[label]}s to {target[label]}s
#PREFIX:      {source[beacon_pattern]}
#TARGET:      {target[beacon_pattern]}
"""


def print_header(**fields):
    print(beacon_header.format(**fields))


def print_link(source='', target='', annotation=''):
    print('|'.join([source, annotation, target]))
