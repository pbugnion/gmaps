
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

import yaml
import pkg_resources
import numpy as np
import os

DATA_DIR = "data"
METADATA_FNAME = "metadata.yaml"

def _load_metadata():
    with pkg_resources.resource_stream(__name__, METADATA_FNAME) as f: 
        datasets = yaml.load(f)
    return datasets

def list_datasets():
    metadata = _load_metadata()
    return metadata.keys()

    metadata = _load_metadata()
    return metadata[dataset_name]

def load_dataset(dataset_name):
    metadata = _load_metadata()
    fname = metadata[dataset_name]["data_file"]
    fpath = os.path.join(DATA_DIR, fname)
    with pkg_resources.resource_stream(__name__, fpath) as f:
        data = np.genfromtxt(f, delimiter=",", names=True)
    return data

