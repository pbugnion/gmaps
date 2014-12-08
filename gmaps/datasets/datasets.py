
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
    f = pkg_resources.resource_stream(__name__, METADATA_FNAME)
    datasets = yaml.load(f)
    f.close()
    return datasets

def list_datasets():
    metadata = _load_metadata()
    return metadata.keys()

def load_dataset(dataset_name):
    metadata = _load_metadata()
    fname = metadata[dataset_name]["data_file"]
    fpath = os.path.join(DATA_DIR, fname)
    f = pkg_resources.resource_stream(__name__, fpath)
    data = np.genfromtxt(f, delimiter=",", names=True)
    f.close()
    return data

