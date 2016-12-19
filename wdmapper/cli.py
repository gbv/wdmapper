# -*- coding: utf-8 -*-
"""Wraps wdmapper as command line client."""

from __future__ import unicode_literals, print_function
import argparse
import sys

import wdmapper
from .exceptions import WdmapperError


def parse_args(argv):
    """parse wdmapper command line arguments."""

    parser = argparse.ArgumentParser(
        prog='wdmapper',
        description="Manage Wikidata authority file mappings.",
        epilog="See <https://github.com/gbv/wdmapper#readme> for details."
    )

    parser.add_argument('-V', '--version', action='store_true',
                        help='show version number of this script')
    parser.add_argument('-f', '--from', dest='format', metavar='NAME',
                        help='input format (default: csv)')
    parser.add_argument('-t', '--to', metavar='NAME',
                        help='output format (default: beacon)')
    parser.add_argument('-H', '--no-header', dest='no_header', action='store_true',
                        help='read CSV without header')
    parser.add_argument('-i', '--input', default='-', metavar='IN',
                        help='input file to read from (default: - for STDIN)')
    parser.add_argument('-o', '--output', default='-', metavar='OUT',
                        help='output file to write to (default: - for STDOUT)')
    parser.add_argument('-s', '--sort', action='store_true',
                        help='sort mappings for normalized output')
    parser.add_argument('-l', '--limit', metavar='N', type=int, default=0,
                        help='maximum number of mappings to process')
    parser.add_argument('-n', '--no-edit', dest='edit', action='store_false', default=True,
                        help='don\'t perform any edits on Wikidata')

    parser.add_argument('command', nargs='?',
                        help=' / '.join(wdmapper.commands))
    parser.add_argument('properties', nargs='*', metavar='property',
                        help='source / target property given by id, URL, URI, or label')

    args = parser.parse_args(argv)

    if not argv or args.command == 'help':
        parser.print_help()
        sys.exit(1)

    if args.version:
        print("wdmapper %s" % wdmapper.__version__)
        sys.exit(0)

    if args.command not in wdmapper.commands:
        if len(args.properties) < 2:
            if args.command:
                args.properties.insert(0, args.command)
                args.command = 'property'
            else:
                args.command = 'echo'

    return args


def run(*args):
    """Execute wdmapper from module with command line arguments."""

    try:
        args = parse_args(list(args))
        wdmapper.wdmapper(args)
    except WdmapperError as e:
        print(e.message(), file=sys.stderr)
        sys.exit(1)


def main():
    """Run wdmapper from command line after installation."""

    args = map(lambda arg: arg.decode(sys.stdout.encoding), sys.argv[1:])
    run(*args)
