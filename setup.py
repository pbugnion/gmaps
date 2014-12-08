#!/usr/bin/env python

from setuptools import setup
import os
import IPython

import gmaps
version = gmaps.__version__

long_description = """

gmaps
=====

gmaps is a plugin for including interactive Google maps in the IPython Notebook.

Let's plot a heatmap of taxi pickups in San Francisco:

.. code:: python

    In [1]: import gmaps

    # load a Numpy array of (latitude, longitude) pairs
    In [2]: data = gmaps.datasets.load_dataset('taxi_rides') 
            
    In [3]: map = gmaps.heatmap(data)
            gmaps.display(map)

Installation
------------

Using pip or easy_install
^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way to install `gmaps` is with pip::

    $ pip install gmaps

or, if you don't have pip,::

    $ easy_install gmaps

You may need to run these commands as root if you are using the system wide Python installation.

Development version
^^^^^^^^^^^^^^^^^^^

The development version can be installed by cloning the git repository by running::

    $ git clone https://github.com/pbugnion/gmaps.git

Change to the project's root directory and run::

    $ python setup.py install

Alternatively, if you are planning on doing development with `gmaps`, install `gmaps` in
development mode using::

    $ python setup.py install_data
    $ python setup.py develop

Getting started
---------------

Currently, only heatmaps are supported. Draw a heatmap by passing a list of (latitude, longitude)
pairs to the heatmap command.

There are example notebooks in the examples directory. You can view these on `nbviewer
<http://nbviewer.ipython.org/github/pbugnion/gmaps/blob/master/examples/ipy3/>`_,
but note that you need to download the notebook to actually see the Google Map.

Issue reporting and contributing
--------------------------------

Report issues using the `github issue tracker <https://github.com/pbugnion/gmaps/issues>`_.

Contributions are welcome. Read the CONTRIBUTING guide to learn how to contribute.
"""

classifiers = [
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Telecommunications Industry',
    'License :: OSI Approved :: BSD License',
    'Framework :: IPython',
    'Programming Language :: Python',
    'Topic :: Software Development',
    'Topic :: Scientific/Engineering',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: JavaScript',
    'Topic :: Scientific/Engineering :: GIS',
    'Topic :: Scientific/Engineering :: Visualization',
    ]


def write_readme():
    """
    Create README file from LONG_DESCRIPTION, replacing non-standard
    bits of re-structured text.
    """
    with open("README.rst","w") as f:
        f.write("""\
.. Automatically generated from LONG_DESCRIPTION keyword in 
.. setup.py. Do not edit directly.\
""")
        f.write(long_description.replace(".. code:: python","::"))


if __name__ == "__main__":

    write_readme()

    ipython_dir = IPython.get_ipython().ipython_dir

    setup(name="gmaps",
          version=version,
          description="IPython plugin for Google Maps JavaScript API",
          long_description=long_description,
          author="Pascal Bugnion",
          author_email="pascal@bugnion.org",
          data_files=[(os.path.join(ipython_dir, "nbextensions/gmaps_js"),
              ["gmaps/js/heatmap_view.js"])],
          classifiers=classifiers,
          packages=["gmaps", "gmaps.datasets"],
          package_dir={"gmaps.datasets" : "gmaps/datasets" },
          package_data={"gmaps.datasets": ["metadata.yaml","data/*.csv"]},
          url=r"https://github.com/pbugnion/gmaps",
          license="BSD License", 
          platforms=["Linux", "Mac OS", "Windows"]
    )
