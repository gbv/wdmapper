# -*- coding: utf-8 -*-
"""Functions to use wdmapper as command line client."""

from __future__ import unicode_literals
import argparse
import sys

import wdmapper
from .exceptions import WdmapperError
from .version import __version__

input_formats = ['csv']
output_formats = ['beacon']


def parse_args(argv):
    """parse command line arguments."""

    commands = ['get', 'echo', 'check', 'diff', 'add', 'sync', 'property', 'help']

    parser = argparse.ArgumentParser(
        prog='wdmapper',
        description="Manage Wikidata authority file mappings.",
        epilog="See <https://github.com/gbv/wdmapper#readme> for details."
    )

    parser.add_argument('-V', '--version', action='store_true',
                        help='show version number of this script')
    parser.add_argument('-i', '--input', default='-', metavar='IN',
                        help='input file to read from (default: - for STDIN)')
    parser.add_argument('-f', '--from', dest='format', metavar='F',
                        help='input format (default: csv)')
    parser.add_argument('-t', '--to', metavar='F',
                        help='output format (default: beacon)')
    parser.add_argument('-H', '--no-header', dest='csv_header', action='store_true',
                        help='read CSV without header')
    parser.add_argument('-l', '--limit', metavar='N', type=int, default=0,
                        help='maximum number of mappings to process')
    parser.add_argument('-n', '--no-edit', dest='edit', action='store_false', default=True,
                        help='don\'t perform any edits on Wikidata')

    parser.add_argument('command', nargs='?',
                        help=' / '.join(commands))
    parser.add_argument('properties', nargs='*', metavar='property',
                        help='source / target property given by id, URL, URI, or label')

    args = parser.parse_args(argv)

    if not argv or args.command == 'help':
        parser.print_help()
        sys.exit(1)

    if args.version:
        print("wdmapper %s" % __version__)
        sys.exit(0)

    if args.format:
        args.format = args.format.lower()
        if args.format not in input_formats:
            raise WdmapperError('input format must be one of: ' + ', '.join(in_formats))

    if args.to:
        args.to = args.to.lower()
        if args.to not in input_formats:
            raise WdmapperError('output format must be one of: ' + ', '.join(out_formats))
            raise WdmapperError('unknown output format: ' + args.to)

    if args.command not in commands:
        if len(args.properties) < 2:
            args.properties.insert(0, args.command)
            args.command = 'property'
        else:
            raise WdmapperError("command must be one of " + ", ".join(commands))

    return args


def run(*args):
    """Execute wdmapper from module with command line arguments."""

    try:
        args = parse_args(list(args))
        wdmapper.wdmapper(args)
    except WdmapperError as e:
        e.print_and_exit()


def main():
    """Run from command line after installation."""

    args = map(lambda arg: arg.decode(sys.stdout.encoding), sys.argv[1:])
    run(*args)
