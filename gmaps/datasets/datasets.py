
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

import json
import os
import csv

import pkg_resources

DATA_DIR = "data"
METADATA_FNAME = "metadata.json"

def _load_metadata():
    f = pkg_resources.resource_stream(__name__, METADATA_FNAME)
    datasets = json.load(f)
    f.close()
    return datasets

def _read_rows(f):
    f.readline() # skip header line
    reader = csv.reader(f)
    rows = [ map(float, row) for row in reader ]
    return rows

def list_datasets():
    metadata = _load_metadata()
    return metadata.keys()

def load_dataset(dataset_name):
    metadata = _load_metadata()
    fname = metadata[dataset_name]["data_file"]
    fpath = os.path.join(DATA_DIR, fname)
    f = pkg_resources.resource_stream(__name__, fpath)
    data = _read_rows(f)
    f.close()
    return data
