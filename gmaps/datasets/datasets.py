
"""
datasets.py
===========

Access geographical datasets.

Commands
--------
    list_datasets() : get a list of available datasets.
    describe_dataset(dataset_name) : get metadata on specified
        dataset.
    load_dataset(dataset_name) : load dataset. Returns a numpy array.
"""

import csv
import codecs

from six.moves.urllib.request import urlopen

METADATA = {
    "taxi_rides": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/taxi_data.csv",  # noqa
        "description": "Taxi pickup location data in San Francisco"
    },
    "earthquakes": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/earthquakes.csv",  # noqa
        "description": ("All recorded earthquakes in 30 days "
                        "starting on 12th November 2014")
    },
    "acled_africa": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/acled_africa.csv",  # noqa
        "description": "Recorded incidents of political violence in Africa",
        "source": "http://www.acleddata.com"
    },
    "nuclear_plants": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/nuclear_power_plants.csv",  # noqa
        "description": "All nuclear power plants worldwide",
        "source": "IAEA (https://www.iaea.org/pris/)"
    },
    "starbucks_uk": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/starbucks_uk.csv",  # noqa
        "description": "All Starbucks in the UK (September 2016)",
        "source": "http://ratings.food.gov.uk"
    },
    "kfc_uk": {
        "url": "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/kfc_uk.csv",  # noqa
        "description": "All KFC restaurants in the UK (September 2016)",
        "source": "http://ratings.food.gov.uk"
    }
}


def _read_rows(f):
    f.readline()  # skip header line
    reader = csv.reader(codecs.iterdecode(f, "utf-8"))
    rows = [tuple(map(float, row)) for row in reader]
    return rows


def list_datasets():
    """
    List of datasets available
    """
    return METADATA.keys()


def load_dataset(dataset_name):
    """
    Fetch a dataset, returning an array of tuples.
    """
    url = METADATA[dataset_name]["url"]
    f = urlopen(url)
    data = _read_rows(f)
    f.close()
    return data
