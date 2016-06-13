
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
    "taxi_rides" : {
        "url" : "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/taxi_data.csv",
        "description" : "Taxi pickup location data in San Francisco"
    },
    "earthquakes" : {
        "url" : "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/earthquakes.csv",
        "description" : "All recorded earthquakes in 30 days starting on 12th November 2014"
    },
    "acled_africa": {
        "url" : "https://s3-eu-west-1.amazonaws.com/jupyter-gmaps-examples/acled_africa.csv",
        "description" : "All recorded incidents of political violence in Africa",
        "source": "http://www.acleddata.com"
    }
}

def _read_rows(f):
    f.readline() # skip header line
    reader = csv.reader(codecs.iterdecode(f, "utf-8"))
    rows = [tuple(map(float, row)) for row in reader]
    return rows

def list_datasets():
    return METADATA.keys()

def load_dataset(dataset_name):
    url = METADATA[dataset_name]["url"]
    f = urlopen(url)
    data = _read_rows(f)
    f.close()
    return data
