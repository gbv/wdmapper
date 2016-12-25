# -*- coding: utf-8 -*-
"""Manage Wikidata authority file mappings."""

from __future__ import unicode_literals, print_function
import sys
import os
import io
import codecs
import itertools

from .exceptions import WdmapperError, ArgumentError
from .format import beacon, csv
from . import wikidata

__version__ = '0.0.4'
"""Version number of module wdmapper."""

commands = ['get', 'head', 'check', 'diff', 'convert', 'add', 'sync', 'help']
"""List if available commands."""

formats = {f.name: f for f in [csv, beacon]}
"""Dict of input/output format names mapped to corresponding modules."""


def readers():
    return dict((f, formats[f]) for f in formats
                if hasattr(formats[f],'reader'))


def writers():
    return dict((f, formats[f]) for f in formats
                if hasattr(formats[f],'writer'))


def _get_links(args):
    """Get links from Wikidata.

    Returns:
        (dict, iter): Mapping metadata and link iterator
    """

    return _get_links_header(args), wikidata.get_links(**args.__dict__)


def _get_links_header(args):

    # build meta fields
    meta = {
        'name': '{target[label]}',
        'description': 'Mapping from {source[label]}s to {target[label]}s',
        'prefix': '{source[template]}',
        'target': '{target[template]}'
    }

    if len(args.properties) > 1:
        props = {'source': args.properties[0], 'target': args.properties[1]}
    else:
        props = {'source': {'template': 'http://www.wikidata.org/entity/',
                            'label': 'Wikidata ID'},
                 'target': args.properties[0]}

    for f in meta:
        try:
            meta[f] = meta[f].format(**props)
        except KeyError:
            meta[f] = None

    return meta


def _get_reader(args):
    reader = csv.reader(args.input, header=not args.no_header)
    # TODO: args.properties => meta.source/meta.target
    if args.limit:
        reader = itertools.islice(reader, args.limit)
    return {}, reader


def _get_diff(args):
    in_meta, in_links = _get_reader(args)
    wd_meta, wd_links = _get_links(args)
    # TODO: in_meta must be empty or same as wd_meta!

    # we could use difflib but set operations work as well and look better
    a = set(list(wd_links))
    b = set(list(in_links))

    delta = [('-', l) for l in a - b] + [('+', l) for l in b - a]
    delta = sorted(delta, key=lambda l: l[1])

    return wd_meta, [delta]


def _check_mappings(args):
    in_meta, in_links = _get_reader(args)
    # TODO: set meta from args.properties!
    return in_meta, wikidata.get_deltas(in_links, **args.__dict__)


def _check_args(command, args):
    """Check and normalize wdmapper arguments.

    Raises:
       wdmapper.exceptions.ArgumentError
    """

    if command not in commands:
        raise ArgumentError('command', allow=commands)

    # 'from' is a reserved word so better rename the argument to 'format'
    if hasattr(args, 'from'):
        args.format = getattr(args, 'from')
        delattr(args, 'from')

    if args.format:
        args.format = args.format.lower()
        allow = readers().keys()
        if args.format not in allow:
            raise ArgumentError('input format', allow=allow)

    if args.to:
        args.to = args.to.lower()
        allow = writers().keys()
        if args.to not in allow:
            raise ArgumentError('output format', allow=allow)

    if command == 'diff':
        args.sort = True

    if not hasattr(args, 'writer'):
        args.writer = None


def wdmapper(command=None, **args):
    """Execute wdmapper."""

    # convert arguments into an object for access via dot-notation
    arguments = type(str('Arguments'), (object,), {})()
    for name in args:
        setattr(arguments, name, args[name])
    args = arguments

    _check_args(command, args)

    PY3 = sys.version_info[0] == 3

    # open input file or stream
    if (args.input and args.input != '-'):
        if not args.format:
            name, ext = os.path.splitext(args.input)
            try:
                args.format = [f for f in readers().values()
                               if f.extension == ext][0].name
            except IndexError:
                pass
        args.input = io.open(args.input, 'r', encoding='utf8')
    elif sys.stdin.isatty() or PY3:
        args.input = sys.stdin
    else:
        args.input = codecs.getreader('utf-8')(sys.stdin)

    # open output file or stream
    if (args.output and args.output != '-'):
        if not args.to:
            name, ext = os.path.splitext(args.output)
            try:
                args.to = [f for f in writers().values()
                           if f.extension == ext][0].name
            except IndexError:
                pass
        args.output = io.open(args.output, 'w', encoding='utf8')
    elif sys.stdout.isatty() or PY3:
        args.output = sys.stdout
    else:
        args.output = codecs.getwriter('utf-8')(sys.stdout)

    # look up given properties
    args.properties = [wikidata.get_property(p, cache=args.cache, debug=args.debug)
                       for p in args.properties]
    for p in args.properties:
        if args.debug:
            print(repr(p), file=sys.stderr)

    # execute selected command
    if command == 'get':
        meta, links = _get_links(args)
    elif command == 'head':
        meta = _get_links_header(args)
        links = []
    elif command == 'check':
        meta, deltas = _check_mappings(args)
    elif command == 'diff':
        meta, deltas = _get_diff(args)
    elif command == 'convert':
        meta, links = _get_reader(args)

    # initialize writer
    if not args.writer:
        header = (command == 'about' or not args.no_header)
        if args.to == 'csv':
            args.writer = csv.writer(args.output, header=header)
        else:
            args.writer = beacon.writer(args.output, header=header)

    # emit output
    if command in ['get', 'head', 'convert']:
        args.writer.init(meta)
        for link in links:
            args.writer.write_link(link)
    elif command in ['diff', 'check']:
        args.writer.init(meta)
        for delta in deltas:
            args.writer.write_delta(delta)
    else:
        if command in ['add','sync']:
            wikidata.setup_pywikibot()
        raise WdmapperError("command %s is not implemented yet" % command)
