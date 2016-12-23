# -*- coding: utf-8 -*-
"""Manage Wikidata authority file mappings."""

from __future__ import unicode_literals, print_function
import sys
import os
import io
import codecs

from .exceptions import WdmapperError, ArgumentError
from .sparql import sparql_query
from .property import Property
from .link import Link
from .format import beacon, csv

__version__ = '0.0.3'
"""Version number of module wdmapper."""

commands = ['get', 'convert', 'check', 'diff', 'add', 'sync', 'property', 'help']
"""List if available commands."""

formats = {f.name: f for f in [csv, beacon]}
"""Dict of input/output format names mapped to corresponding modules."""


def readers():
    return dict((f, formats[f]) for f in formats
                if hasattr(formats[f],'reader'))


def writers():
    return dict((f, formats[f]) for f in formats
                if hasattr(formats[f],'writer'))


def setup_pywikibot():
    """initialize pywikibot connected to wikidata"""
    global pywikibot
    global site
    global repo
    try:
        import pywikibot
    except RuntimeError as e:
        # create user-config.py if needed
        if os.path.exists('user-config.py'):
            raise
        # print('user-config.py created')
        file = open('user-config.py', 'w')
        file.write("\n".join([
            "mylang = 'wikidata'",
            "family = 'wikidata'",
            "# usernames['wikidata']['wikidata'] = u'YOUR-USERNAME'",
            "console_encoding = 'utf-8'", ""
        ]))
        file.close()
        import pywikibot
        site = pywikibot.Site()
        repo = site.data_repository()


def command_get(args):

    metafields = {
        'name': '{target[label]}',
        'description': 'Mapping from {source[label]}s to {target[label]}s',
        'prefix': '{source[beacon_pattern]}',
        'target': '{target[beacon_pattern]}'
    }

    props = {'source': args.properties[0]}
    if len(args.properties) > 1:
        props['target'] = args.properties[1]

    for f in metafields:
        try:
            metafields[f] = metafields[f].format(**props)
        except KeyError:
            metafields[f] = None

    writer = create_writer(args, metafields)

    for link in get_links_from_wikidata(args):
        writer.write_link(link)


def create_writer(args, metafields={}):
    header = not args.no_header
    if args.to == 'csv':
        return csv.writer(args.output, header=header)
    else:
        return beacon.writer(args.output, header=header, **metafields)


def command_diff(args):
    input_links = csv.reader(args.input, header=not args.no_header)
    wikidata_links = get_links_from_wikidata(args)

    # we could use difflib but set operations work as well and look better
    a = set(list(wikidata_links))
    b = set(list(input_links))

    delta = [('-', l) for l in a - b] + [('+', l) for l in b - a]
    delta = sorted(delta, key=lambda l: l[1])

    args.no_header = True  # TODO: keep header?
    writer = create_writer(args, {})

    for op, link in delta:
        args.output.write(op + ' ')
        writer.write_link(link)


def get_links_from_wikidata(args):
    properties = args.properties

    if len(properties) == 1:
        sparql = """\
SELECT ?item ?target WHERE {{
    ?item wdt:{target[id]} ?target .
}}"""
        wd = Property({
                      'label':'Wikidata ID',
                      'pattern':'http://www.wikidata.org/entity/'
                      })
        fields = {'source':wd, 'target':properties[0]}
    else:
        sparql = """\
SELECT ?item ?source ?target WHERE {{
    ?item wdt:{source[id]} ?source .
    ?item wdt:{target[id]} ?target .
}}"""
        fields = {'source':properties[0], 'target':properties[1]}

    query = sparql.format(**fields)
    if (args.limit):
        query += ' LIMIT {:d}'.format(args.limit)
    if (args.sort):
        query += '\nORDER BY ?source ?target'

    cache = not args.no_cache
    res = sparql_query(query, cache=cache)

    for m in res:
        qid = m['item'].split('/')[-1]
        if len(properties) == 1:
            yield Link(qid, m['target'])
        else:
            yield Link(m['source'], m['target'], qid)

# TODO: lookup item with source_property = mapping.source in Wikidata
# TODO: check for existence of statement with target_property
# TODO: add statement with target_property = args.target unless it exists


def command_property(args):
    for p in args.properties:
        print(p)


def command_convert(args):

    if args.properties:
        return

    header = not args.no_header
    reader = csv.reader(args.input, header=header)

    # TODO: add metafields if read
    writer = create_writer(args, {})

    for link in reader:
        writer.write_link(link)


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
    cache = not args.no_cache
    args.properties = [Property.lookup(p, cache=cache) for p in args.properties]

    # execute command
    if command == 'property':
        command_property(args)

    elif command == 'get':
        command_get(args)

    elif command == 'convert':
        command_convert(args)

    elif command == 'diff':
        command_diff(args)

    else:
        if command in ['add','sync']:
            setup_pywikibot()
        raise WdmapperError("command %s is not implemented yet" % args.command)
