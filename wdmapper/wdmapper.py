# -*- coding: utf-8 -*-
"""Manage Wikidata authority file mappings."""

from __future__ import unicode_literals
import sys
import os
import io
import csv

from .exceptions import WdmapperError
from .sparql import sparql_query
from .property import Property
from . import beacon


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
    properties = args.properties

    if len(properties) == 1:
        sparql = """\
SELECT ?item ?targetId WHERE {{
    ?item wdt:{target[id]} ?targetId .
}}"""
        wd = Property({
                      'label':'Wikidata ID',
                      'pattern':'http://www.wikidata.org/entity/'
                      })
        fields = {'source':wd, 'target':properties[0]}
    else:
        sparql = """\
SELECT ?item ?sourceId ?targetId WHERE {{
    ?item wdt:{source[id]} ?sourceId .
    ?item wdt:{target[id]} ?targetId .
}}"""
        fields = {'source':properties[0], 'target':properties[1]}

    query = sparql.format(**fields)
    if (args.limit):
        query += ' LIMIT {:d}'.format(args.limit)

    beacon.print_header(**fields)

    res = sparql_query(query)

    for m in res:
        qid = m['item'].split('/')[-1]
        if len(properties) == 1:
            beacon.print_link(source=qid, target=m['targetId'])
        else:
            beacon.print_link(source=m['sourceId'], target=m['targetId'], annotation=qid)


def read_csv(csv_file, callback, header=True):
    if (header):
        header = ['source', 'target', 'annotation']

    for row in csv.reader(iter(csv_file.readline, '')):
        if not header:
            header = row
        else:
            mapping = []
            mapping = {k: v.strip() for k, v in zip(header, row) if v != ''}
            callback(mapping)


def process_mapping(mapping):
    print('{m[source]} | {m[target]}'.format(m=mapping))

    # TODO: lookup item with source_property = mapping.source in Wikidata
    # TODO: check for existence of statement with target_property
    # TODO: add statement with target_property = args.target unless it exists


def command_property(args):
    for p in args.properties:
        print(p)


def command_echo(args):
    filename = args.input
    if (filename and filename != '-'):
        input_file = io.open(filename, 'r', encoding='utf8')
    else:
        input_file = sys.stdin

    if not args.properties:
        # read mappings from input by default
        read_csv(input_file, process_mapping, header=args.csv_header)


def wdmapper(args):
    """Execute wdmapper with arguments."""

    # look up given properties
    args.properties = [Property.lookup(p) for p in args.properties]

    if args.command == 'property':
        command_property(args)

    elif args.command == 'get':
        command_get(args)

    elif args.command == 'echo':
        command_echo(args)

    else:
        if args.command in ['add','sync']:
            setup_pywikibot()
        raise WdmapperError("command %s is not implemented yet" % args.command)
