
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
    },
    "england-counties": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/england-counties.geo.json",  # noqa
        "description": ("Counties and unitary authorities boundaries " +
                        "for England and Wales"),
        "source": "https://data.gov.uk/dataset/counties-and-unitary-authorities-december-2015-full-extent-boundaries-in-england-and-wales"  # noqa
    },
    "us-states": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/us-states.geo.json",  # noqa
        "description": "US state boundaries",
        "source": "http://eric.clst.org/Stuff/USGeoJSON"  # noqa
    },
    "us-counties": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/us-counties.geo.json",  # noqa
        "description": "US county boundaries",
        "source": "http://eric.clst.org/Stuff/USGeoJSON"  # noqa
    },
    "india-states": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/india-states.geo.json",  # noqa
        "description": "India state boundaries",
        "source": "https://github.com/geohacker/india"  # noqa
    },
    "brazil-states": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/brazil-states.geo.json",  # noqa
        "description": "Brazil state boundaries",
        "source": "https://github.com/codeforamerica/click_that_hood/blob/master/public/data/brazil-states.geojson (No license specified, so use with care)"  # noqa
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
    """
    Fetch a geometry.

    :returns:
        A python dictionary containing the geometry.

    :Examples:

    >>> import gmaps
    >>> import gmaps.geojson_geometries
    >>> gmaps.configure(api_key="AIza...")
    >>> countries_geojson = gmaps.geojson_geometries.load_geometry('countries')

    >>> fig = gmaps.figure()
    >>> gini_layer = gmaps.geojson_layer(countries_geojson)
    >>> fig.add_layer(gini_layer)
    >>> fig
    """
    url = METADATA[geometry_name]["url"]
    reader = codecs.getreader("utf-8")
    f = urlopen(url)
    geometry = json.load(reader(f))
    f.close()
    return geometry
