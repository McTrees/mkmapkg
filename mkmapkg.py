#!/usr/bin/env python3
"""mkmapkg
This script takes a graphml from yed and a background image, and creates a mapkg file.

Usage:
mkmapkg
"""


def parse_args():
    from argparse import ArgumentParser, FileType
    import sys
    parser = ArgumentParser(description="Create a mapkg file from a graphml from yed.")
    parser.add_argument('graphml', help="The graphml file to use for creating map data")
    parser.add_argument('image', help="The background image to use for the map")
    parser.add_argument('-o', '--output', default="map.mapkg", help="The output mapkg file to use (default %(default)s).")
    parser.add_argument('-v', '--verbose', action="store_true", help="Log extra informational messages.")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def create_node_data(path):
    from bs4 import BeautifulSoup
    with open(path, "r") as fp:
        xmlstr = fp.read()

def main():
    args = parse_args()
    node_data = create_node_data(args.graphml)


if __name__ == "__main__":
    main()
