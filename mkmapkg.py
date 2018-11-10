#!/usr/bin/env python
"""mkmapkg
This script takes a graphml from yed and a background image, and creates a mapkg file.

Usage:
mkmapkg
"""

from argparse import ArgumentParser, FileType
import sys
import json

import lxml
from bs4 import BeautifulSoup


def parse_args():
    parser = ArgumentParser(description="Create a mapkg file from a graphml from yed.")
    parser.add_argument('graphml', help="The graphml file to use for creating map data")
    parser.add_argument('image', help="The background image to use for the map")
    parser.add_argument('-o', '--output', default="map.mapkg", help="The output mapkg file to use (default %(default)s).")
    parser.add_argument('-v', '--verbose', action="store_true", help="Log extra informational messages.")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def get_soup(path):
    try:
        with open(path, "r") as fp:
            xmlstr = fp.read()
    except FileNotFoundError:
        print("Error: file {} does not exist.".format(path), file=sys.stderr)
        sys.exit(1)
    soup = BeautifulSoup(xmlstr, "xml")
    if soup.graphml is None:
        print("Error: file {} is not a valid graphml file.".format(path), file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_args()
    soup = get_soup(args.graphml)


if __name__ == "__main__":
    main()
