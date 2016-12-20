# -*- coding: utf-8 -*-
"""Manage Wikidata authority file mappings."""

from __future__ import unicode_literals
import sys
import os
import io

from .exceptions import WdmapperError, ArgumentError
from .sparql import sparql_query
from .property import Property
from .link import Link
from .format import beacon, csv

__version__ = '0.0.1'
"""Version number of module wdmapper."""

commands = ['get', 'echo', 'check', 'diff', 'add', 'sync', 'property', 'help']
"""List if available commands."""


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

    if args.to == 'beacon':
        writer = beacon.writer(args.output, **metafields)
    else:
        writer = csv.writer(args.output)

    for link in get_links_from_wikidata(args):
        writer.write_link(link)


def command_diff(args):
    # TODO: don't limit
    wdlinks = get_links_from_wikidata(args)
    reader = csv.reader(args.input, header=not args.no_header)
    # TODO: sort links and use difflib


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

    res = sparql_query(query)

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


def command_echo(args):

    if args.properties:
        return

    reader = csv.reader(args.input, header=not args.no_header)

    if args.to == 'beacon':
        metafields = {}  # TODO
        writer = beacon.writer(sys.stdout, **metafields)
    else:
        writer = csv.writer(sys.stdout, header=not args.no_header)

    for link in reader:
        writer.write_link(link)


def check_args(args):
    """Check and normalize wdmapper arguments."""

    formats = {'csv':csv, 'beacon':beacon}

    if args.format:
        args.format = args.format.lower()
        allow = [f for f in formats if hasattr(formats[f],'reader')]
        if args.format not in allow:
            raise ArgumentError('input format', allow=allow)

    if args.to:
        args.to = args.to.lower()
        allow = [f for f in formats if hasattr(formats[f],'writer')]
        if args.to not in allow:
            raise ArgumentError('output format', allow=allow)

    if args.command not in commands:
        raise ArgumentError('command', allow=commands)


def wdmapper(args):
    """Execute wdmapper with arguments."""

    check_args(args)

    # open input file
    if (args.input and args.input != '-'):
        args.input = io.open(args.input, 'r', encoding='utf8')
    else:
        args.input = sys.stdin

    # open output file
    if (args.output and args.output != '-'):
        args.output = io.open(args.output, 'w', encoding='utf8')
    else:
        args.output = sys.stdout

    # look up given properties
    args.properties = [Property.lookup(p) for p in args.properties]

    # execute command
    if args.command == 'property':
        command_property(args)

    elif args.command == 'get':
        command_get(args)

    elif args.command == 'echo':
        command_echo(args)

    elif args.command == 'diff':
        command_diff(args)

    else:
        if args.command in ['add','sync']:
            setup_pywikibot()
        raise WdmapperError("command %s is not implemented yet" % args.command)
