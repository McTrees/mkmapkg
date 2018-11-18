# mkmapkg
Script for making a mapkg file from a yEd-graphml file, for use with
the CHS map site.

## Installation
In a venv or otherwise, install the packages listed in `requirements.txt` as follows
```
pip install -r requirements.txt
```

## Usage
```
mkmapkg.py [-h] [-o OUTPUT] [-v] [-w] graphml image

Create a mapkg file from a graphml from yEd.

positional arguments:
  graphml               The graphml file to use for creating map data
  image                 The background image to use for the map

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The output mapkg file to use (default map.mapkg).
  -v, --verbose         Log extra informational messages.
  -w, --overwrite       Overwrite the output file if it already exists.
```
For instance, to create a mapkg file from the graphml file `info.graphml`, with the background image `image.png`, and to output into `info.mapkg`, overwriting if necessary, do the following:
```
mkmapkg.py info.graphml image.png -o info.mapkg -w
```

# License
GPL-3.0; see LICENSE file.
