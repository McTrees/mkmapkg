#!/usr/bin/env python
"""mkmapkg
This script takes a graphml from yed and a background image, and creates a mapkg file.

Usage:
mkmapkg
"""

from argparse import ArgumentParser, FileType
import sys
import json
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("mkmapkg")

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
        logger.error("file %s does not exist.", path)
        sys.exit(1)
    except UnicodeDecodeError:
        logger.error("a unicode decoding error occurred when opening file %s.", path)
        sys.exit(1)
    except:
        logger.error("an error occured when opening file %s.", path)
    soup = BeautifulSoup(xmlstr, "xml")
    if soup.graphml is None:
        logger.error("file %s is not a valid graphml document.", path)
        sys.exit(1)
    return soup


def create_node_data(soup):
    for edge in soup("edge"):
        logger.debug("processing edge %s", edge['id'])
        first_node_id = edge['source']
        second_node_id = edge['target']
        first_node = soup("node", id=first_node_id)
        if first_node is None:
            logger.warning("couldn't find a node with id %s (from edge %s)", first_node_id, edge['id'])
        second_node = soup("node", id=second_node_id)
        if first_node is None:
            logger.warning("couldn't find a node with id %s (from edge %s)", second_node_id, edge['id'])

def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    soup = get_soup(args.graphml)
    node_data = create_node_data(soup)


if __name__ == "__main__":
    main()
