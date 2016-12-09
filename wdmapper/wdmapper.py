import argparse
import sys
import os
import io
import csv

supported_formats = ['CSV']


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
            sys.exit(exception)
        # print('user-config.py created')
        file = open('user-config.py', 'w')
        file.write("\n".join([
            "mylang = 'wikidata'",
            "family = 'wikidata'",
            "# usernames['wikidata']['wikidata'] = u'YOUR-USERNAME'",
            "console_encoding = 'utf-8'",
        ]))
        file.close()
        import pywikibot
        site = pywikibot.Site('en', 'wikipedia')
        repo = site.data_repository()


def wikidata_property(s):
    """check and normalize property value such as 'P32'"""
    # TODO: actually check and normalize
    return s


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


def parse_args(argv):
    """parse command line arguments"""

    parser = argparse.ArgumentParser(description='Manage Wikidata authority file mappings')

    parser.add_argument('-n', dest='edit', action='store_false', default=True,
                        help='don\'t do any edits on Wikidata')
    parser.add_argument('-i', '--input', default='-',
                        help='input file to read from (default: - for STDIN)')
    parser.add_argument('-H', dest='csv_header', action='store_true',
                        help='read CSV without header')
    parser.add_argument('-f', '--format', dest='fmt',
                        help='input format (default: CSV)')
    parser.add_argument('-l', '--limit', dest='lmt', type=int, default=0,
                        help='maximum number of mappings to process')

    parser.add_argument('source', nargs='?',
                        help='source property')
    parser.add_argument('target', nargs='?',
                        help='target property')

    args = parser.parse_args(argv)

    args.limit = args.lmt
    if args.fmt:
        args.format = args.fmt.upper()
        if args.format not in supported_formats:
            sys.exit('unknown format: ' + args.fmt)

    if not argv:
        parser.print_help()
        sys.exit(1)

    return args


def process_mapping(mapping):
    print('{m[source]} | {m[target]}'.format(m=mapping))

    # TODO: lookup item with source_property = mapping.source in Wikidata
    # TODO: check for existence of statement with target_property
    # TODO: add statement with target_property = args.target unless it exists


def run(*argv):
    args = parse_args(argv[1:])

    source_property = wikidata_property(args.source)
    target_property = wikidata_property(args.target)

    setup_pywikibot()

    if (args.input and args.input != '-'):
        input_file = io.open(args.input, 'r', encoding='utf8')
    else:
        input_file = sys.stdin

    if not args.source and not args.target:
        # read mappings from input by default
        read_csv(input_file, process_mapping, header=args.csv_header)

if __name__ == '__main__':
    run(sys.argv[1:])
