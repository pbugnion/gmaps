
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
import codecs

from six.moves.urllib.request import urlopen

METADATA = {
    "countries": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/countries.geo.json",  # noqa
        "description": ("Map of world countries. See also "
                        "`countries-high-resolution` for a higher "
                        "resolution version of this."),
        "source": "https://github.com/datasets/geo-countries"
    },
    "countries-high-resolution": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/countries-high-resolution.geo.json",  # noqa
        "description": ("Map of world countries. See also `countries` "
                        "for a lower resolution version of this."),
        "source": "https://github.com/datasets/geo-countries"
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
    reader = codecs.getreader("utf-8")
    f = urlopen(url)
    geometry = json.load(reader(f))
    f.close()
    return geometry
