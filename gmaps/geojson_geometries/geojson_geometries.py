
"""
geojson_geometries
==================

Access GeoJSON files for common geographical entities (e.g. countries)

Commands
--------
    list_geometries(): get a list of available geometries
    geometry_metadata(geometry): get metadata on specified dataset
    load_geometry(geometry_name): load a GeoJSON dataset
"""

import json

from six.moves.urllib.request import urlopen

METADATA = {
    "countries": {
        "url": "",
        "description": "Map of world countries"
    }
}


def list_geometries():
    """
    List of GeoJSON geometries available
    """
    return METADATA.keys()


def geometry_metadata(geometry_name):
    """
    Information about the geometry.

    This returns a dictionary containing a 'description'.

    :Examples:

    >>> geometry_metadata("countries")
    {'description': 'Map of world countries'}
    """
    metadata = METADATA[geometry_name].copy()
    del metadata["url"]
    return metadata


def load_geometry(geometry_name):
    url = METADATA[geometry_name]["url"]
    with urlopen(url) as f:
        geometry = json.load(f)
    return geometry
