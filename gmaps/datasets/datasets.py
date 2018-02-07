
"""
datasets.py
===========

Access geographical datasets.

Commands
--------
    list_datasets() : get a list of available datasets.
    dataset_metadata(dataset_name) : get metadata on specified
        dataset.
    load_dataset(dataset_name) : load dataset. Returns a numpy array.
"""

import csv
import codecs

from six.moves.urllib.request import urlopen

METADATA = {
    "taxi_rides": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/taxi_data.csv",  # noqa
        "description": "Taxi pickup location data in San Francisco",
        "headers": ["latitude", "longitude"],
        "types": [float, float]
    },
    "earthquakes": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/earthquakes.csv",  # noqa
        "description": ("All recorded earthquakes in 30 days "
                        "starting on 12th November 2014"),
        "headers": ["latitude", "longitude", "magnitude"],
        "types": [float, float, float]
    },
    "acled_africa": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/acled_africa.csv",  # noqa
        "description": "Recorded incidents of political violence in Africa",
        "source": "http://www.acleddata.com",
        "headers": ["latitude", "longitude"],
        "types": [float, float]
    },
    "acled_africa_by_year": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/acled_africa_by_year.csv",  # noqa
        "description": "Recorded incidents of political violence in Africa, with year and number of fatalities",  # noqa
        "source": "http://www.acleddata.com",
        "headers": ["year", "latitude", "longitude", "fatalities"],
        "types": [int, float, float, int]
    },
    "london_congestion_zone": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/london_congestion_zone.csv",  # noqa
        "description": "Central part of the London congestion zone",
        "source": "https://www.google.com/maps/d/u/0/viewer?mid=1EnGO0p4-UuGlSMKyfRrMT21jfRs",  # noqa
        "headers": ["latitude", "longitude"],
        "types": [float, float]
    },
    "nuclear_plants": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/nuclear_power_plants.csv",  # noqa
        "description": "All nuclear power plants worldwide",
        "source": "IAEA (https://www.iaea.org/pris/)",
        "headers": ["latitude", "longitude"],
        "types": [float, float]
    },
    "starbucks_kfc_uk": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/starbucks_kfc_uk.csv",  # noqa
        "description": "All Starbucks and KFCs in the UK (September 2016)",
        "source": "http://ratings.food.gov.uk",
        "headers": ["latitude", "longitude", "chain_name"],
        "types": [float, float, str]
    },
    "gini": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/gini.csv",  # noqa
        "description": "GINI coefficient for most countries",
        "source": "https://www.cia.gov/library/publications/the-world-factbook/rankorder/2172rank.html",  # noqa
        "headers": ["country", "gini"],
        "types": [str, float]
    }
}


def _read_rows(f, column_types):
    f.readline()  # skip header line
    reader = csv.reader(codecs.iterdecode(f, "utf-8"))
    rows = []
    for row in reader:
        typed_row = [
            column_type(cell) for column_type, cell in zip(column_types, row)
        ]
        rows.append(tuple(typed_row))
    return rows


def list_datasets():
    """
    List of datasets available
    """
    return METADATA.keys()


def dataset_metadata(dataset_name):
    """
    Information about the dataset

    This returns a dictionary containing a 'description',
    a list of the dataset headers and optionally information
    about the dataset source.

    :Examples:

    >>> dataset_metadata("earthquakes")
    {'description': 'Taxi pickup location data in San Francisco',
     'headers': ['latitude', 'longitude']}
    """
    metadata = METADATA[dataset_name].copy()
    del metadata["url"]
    return metadata


def load_dataset(dataset_name):
    """
    Fetch a dataset, returning an array of tuples.
    """
    url = METADATA[dataset_name]["url"]
    column_types = METADATA[dataset_name]["types"]
    f = urlopen(url)
    data = _read_rows(f, column_types)
    f.close()
    return data


def load_dataset_as_df(dataset_name):
    """
    Fetch a dataset, returning a pandas dataframe.
    """
    import pandas as pd
    data = load_dataset(dataset_name)
    headers = dataset_metadata(dataset_name)["headers"]
    return pd.DataFrame(data, columns=headers)
