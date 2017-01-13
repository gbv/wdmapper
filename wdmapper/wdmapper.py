# -*- coding: utf-8 -*-
"""Manage Wikidata authority file mappings."""

from __future__ import unicode_literals, print_function
import sys
import os
import io
import codecs
import itertools

from .exceptions import WdmapperError, ArgumentError
from .format import beacon, csv, ntriples
from . import wikidata

__version__ = '0.0.6'
"""Version number of module wdmapper."""

commands = ['get', 'head', 'check', 'diff', 'convert', 'add', 'sync', 'help']
"""List if available commands."""

formats = {f.name: f for f in [csv, beacon, ntriples]}
"""Dict of input/output format names mapped to corresponding modules."""

PY3 = sys.version_info[0] == 3


def readers():
    return dict((f, formats[f]) for f in formats
                if hasattr(formats[f],'Reader'))


def writers():
    return dict((f, formats[f]) for f in formats
                if hasattr(formats[f],'Writer'))


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
        'target': '{target[template]}',
        'relation': '{relation}'
    }

    props = {}
    for name in ['source', 'target', 'relation']:
        if getattr(args, name):
            props[name] = getattr(args, name)

    # direct links
    if 'target' in props and 'source' not in props:
        props['source'] = {'template': 'http://www.wikidata.org/entity/',
                           'label': 'Wikidata ID'}

    for f in meta:
        try:
            meta[f] = meta[f].format(**props)
        except KeyError:
            meta[f] = None

    return meta


def _get_reader(args):
    if args.format == 'beacon':
        meta, reader = beacon.Reader(args.input).read()

        if 'target' in meta:
            target = wikidata.get_property(meta['target'], cache=args.cache, debug=args.debug)
            if args.target and args.target.id != target.id:
                raise WdmapperError('Different target properties %s (argument) and %s (input)!'
                                    % (args.target.id, target.id))
            args.target = target

        if 'prefix' in meta:
            source = meta['prefix']  # TODO: rename
            if source == 'http://www.wikidata.org/entity/':
                source = {'template': 'http://www.wikidata.org/entity/',
                          'label': 'Wikidata ID'}
            else:
                source = wikidata.get_property(source, cache=args.cache, debug=args.debug)
                if args.source and args.source.uri != source.uri:
                    raise WdmapperError('Different source properties %s (argument) and %s (input)!'
                                        % (args.source.id, source.id))
            args.source = source

    else:  # csv as default
        reader = csv.Reader(args.input, header=not args.no_header).links()
        meta = _get_links_header(args)

    if args.limit:
        reader = itertools.islice(reader, args.limit)

    return meta, reader


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
    return in_meta, wikidata.get_deltas(links=in_links, **args.__dict__)


def _check_args(command, args_dict):
    """Check and normalize wdmapper arguments.

    Raises:
       wdmapper.exceptions.ArgumentError
    """

    if command not in commands:
        raise ArgumentError('command', allow=commands)

    # convert arguments into an object for access via dot-notation
    args = type(str('Arguments'), (object,), {})()
    for name in ['source', 'target',
                 'format', 'to', 'input', 'output', 'writer',
                 'sort', 'limit', 'relation', 'dry', 'cache',
                 'debug', 'no_header']:
        setattr(args, name, args_dict[name] if name in args_dict else None)

    # 'from' is a reserved word so better rename the argument to 'format'
    if 'from' in args_dict:
        args.format = args_dict['from']

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
    else:
        args.to = 'beacon'

    if command == 'diff' and args.limit:
        args.sort = True

    if args.debug and not callable(args.debug):
        args.debug = lambda s: print(s, '\n', file=sys.stderr)

    prefixes = {'skos:': 'http://www.w3.org/2004/02/skos/core#',
                'owl:': 'http://www.w3.org/2002/07/owl#',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}
    if args.relation:
        for prefix, uri in prefixes.items():
            if args.relation[:len(prefix)] == prefix:
                args.relation = uri + args.relation[len(prefix):]
                break

    return args


def wdmapper(command=None, **args):
    """Execute wdmapper."""

    args = _check_args(command, args)

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

    # look up properties
    for which in ['source', 'target']:
        prop = getattr(args, which)
        if prop is not None:
            prop = wikidata.get_property(prop, cache=args.cache, debug=args.debug)
            setattr(args, which, prop)

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
        args.writer = writers()[args.to].Writer(args.output, header=header)

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
