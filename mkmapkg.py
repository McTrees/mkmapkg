#!/usr/bin/env python
"""mkmapkg
This script takes a graphml from yed and a background image, and creates a mapkg file.

Usage:
mkmapkg
"""

import argparse
import sys
import io
import json
import zipfile

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("mkmapkg")

import lxml
from bs4 import BeautifulSoup

MAPKG_HEADER = b"MAPKG 0.1"

def parse_args():
    parser = argparse.ArgumentParser(description="Create a mapkg file from a graphml from yed.")
    parser.add_argument('graphml', help="The graphml file to use for creating map data")
    parser.add_argument('image', help="The background image to use for the map")
    parser.add_argument('-o', '--output', default="map.mapkg", help="The output mapkg file to use (default %(default)s).")
    parser.add_argument('-v', '--verbose', action="store_true", help="Log extra informational messages.")
    parser.add_argument('-w', '--overwrite', action="store_true", help="Overwrite the output file if it already exists.")
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

def process_edge_end(soup, node_id, edge):
    node = soup.find("node", id=node_id)
    if node is None:
        logger.error("couldn't find a node with id %s (from edge %s)", first_node_id, edge['id'])
        sys.exit(1)
    node_label = node.find("y:NodeLabel")
    node_names = list(node_label.stripped_strings)
    if len(node_names) > 0:
        return node_names[0]
    else:
        return "["+node_id+"]"

def append_or_create(d, key, item):
    if key in d:
        d[key].append(item)
    else:
        d[key] = [item]

def create_node_data(soup):
    ret = {}
    for edge in soup("edge"):
        logger.debug("processing edge %s", edge['id'])
        first_node = process_edge_end(soup, edge['source'], edge)
        second_node = process_edge_end(soup, edge['target'], edge)
        logger.debug("%s<->%s", first_node, second_node)
        append_or_create(ret, first_node, second_node)
        append_or_create(ret, second_node, first_node)
    return ret

def process_filename(filename):
    if '.' in filename[:-1]:
        return filename
    else:
        return filename + ".mapkg"

def write_mapkg(filename, overwrite, node_data, image_filename):
    if not overwrite:
        try:
            zf = zipfile.ZipFile(filename, 'x')
        except FileExistsError:
            logger.error("File %s already exists!", filename)
            sys.exit(1)
    else:
        zf = zipfile.ZipFile(filename, 'w')
    logger.debug("writing mapkg header")
    zf.writestr("MAPKG", MAPKG_HEADER)
    logger.debug("writing node data")
    node_data_s = json.dumps(node_data)
    zf.writestr("nodes.json", node_data_s)
    logger.debug("writing image")
    zf.write(image_filename, "image.png")
    zf.close()

def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    soup = get_soup(args.graphml)
    node_data = create_node_data(soup)
    write_mapkg(process_filename(args.output), args.overwrite, node_data, args.image)
    print("Done!")
    
if __name__ == "__main__":
    main()
