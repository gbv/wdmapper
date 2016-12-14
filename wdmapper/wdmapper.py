import argparse
import sys
import os
import io
import csv
import re
from .sparql import sparql_query

supported_formats = ['CSV']
supported_commands = ['get', 'echo', 'check', 'diff', 'add', 'sync', 'info', 'help']

__version__ = "0.0.0"


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
            exception = e
            exit(exception)
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


class Property(object):
    """Representation of a Wikidata property"""

    def __init__(self, data):
        self.uri = data['p']
        self.label = data['label']
        self.regex = data['regex']
        self.pattern = data['pattern']

        m = property_pattern.match(self.uri)
        self.id = 'P' + m.group('id')

    def __repr__(self):
        s = "{label} ({id})\n<{uri}>\n".format(**self.__dict__)
        if self.pattern:
            s += self.pattern
        s += "\n"
        if self.regex:
            s += self.regex
        return s


property_pattern = re.compile(r"""
    ^
    (http://www.wikidata.org/entity/
    |https?://www.wikidata.org/wiki/Property:)?
    [Pp]
    (?P<id>[0-9]+)
    $""", re.VERBOSE)

namespace_pattern = re.compile('^[a-z]+:[^<>]+')

get_property_query = """
SELECT ?p ?label ?pattern ?regex WHERE {{
    {0} .
    ?p a wikibase:Property .
    OPTIONAL {{ ?p wdt:P1630 ?pattern }}
    OPTIONAL {{ ?p wdt:P1793 ?regex }}
    SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "{1}" .
        ?p rdfs:label ?label .
    }}
}}
"""


def wikidata_property(s):
    """check and normalize property value such as 'P32'"""

    m = property_pattern.match(s)
    if m:
        # get by property id
        uri = 'http://www.wikidata.org/entity/P' + m.group('id')
        where = 'BIND(<' + uri + '> AS ?p)'
    elif namespace_pattern.match(s):
        # get by formatting URL (P1630)
        # TODO: escape " in URL
        # TODO: only append $1 if not included
        where = '?p wdt:P1630 "%s"' % (s + '$1')
    else:
        # get by name
        # TODO: escape " in name
        # TODO: ignore language
        where = '?p rdfs:label "%s"@en' % s

    query = get_property_query.format(where, 'en')
    # print(query)
    res = sparql_query(query)
    if not res:
        exit("not a property: " + s)
    if len(res) > 1:
        exit("multiple properties: " + s)

    return Property(res[0])


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


def exit(msg, code=1):
    """print error message and exit."""
    sys.stderr.write(msg + "\n")
    sys.exit(code)


def parse_args(argv):
    """parse command line arguments."""

    parser = argparse.ArgumentParser(description='Manage Wikidata authority file mappings.')

    parser.add_argument('-V', '--version', action='store_true',
                        help='show version number of this script')
    parser.add_argument('-i', '--input', default='-', metavar='IN',
                        help='input file to read from (default: - for STDIN)')
    parser.add_argument('-f', '--format', metavar='F',
                        help='input format (default: CSV)')
    parser.add_argument('-H', '--no-header', dest='csv_header', action='store_true',
                        help='read CSV without header')
    parser.add_argument('-l', '--limit', metavar='N', type=int, default=0,
                        help='maximum number of mappings to process')
    parser.add_argument('-n', '--no-edit', dest='edit', action='store_false', default=True,
                        help='don\'t do any edits on Wikidata')

    parser.add_argument('command', nargs='?',
                        help=' / '.join(supported_commands))
    parser.add_argument('source', nargs='?',
                        help='source property (id, URL, URI, or label)')
    parser.add_argument('target', nargs='?',
                        help='target property')

    args = parser.parse_args(argv)

    if not argv or args.command == 'help':
        parser.print_help()
        sys.exit(1)

    if args.version:
        print("wdmapper %s" % __version__)
        sys.exit(0)

    if args.format:
        args.format = args.format.upper()
        if args.format not in supported_formats:
            exit('unknown format: ' + args.fmt)

    if args.command not in supported_commands:
        if args.target is None:
            args.target = args.source
            args.source = args.command
            args.command = 'info'
        else:
            exit("command must be one of " + ", ".join(supported_commands))

    return args


def run(*args):
    args = parse_args(list(args))

    properties = map(lambda p: wikidata_property(p),
                     filter(None, [args.source, args.target]))

    if args.command in ['add','sync']:
        setup_pywikibot()

    if (args.command == 'info'):
        for p in properties:
            print(p)

    elif (args.command == 'echo'):
        if (args.input and args.input != '-'):
            input_file = io.open(args.input, 'r', encoding='utf8')
        else:
            input_file = sys.stdin

        if not args.source and not args.target:
            # read mappings from input by default
            read_csv(input_file, process_mapping, header=args.csv_header)

    else:
        exit("command %s is not implemented yet" % args.command)


def main():
    """entry point to run from command line after installation."""
    run(*(sys.argv[1:]))
