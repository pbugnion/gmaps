.. Automatically generated from LONG_DESCRIPTION keyword in 
.. setup.py. Do not edit directly.

gmaps
=====

gmaps is a plugin for including interactive Google maps in the IPython Notebook.

Let's plot a heatmap of taxi pickups in San Francisco:

::

    In [1]: import gmaps

    # load a Numpy array of (latitude, longitude) pairs
    In [2]: data = gmaps.dataset.load_dataset('taxi_rides') 
            
    In [3]: map = gmaps.heatmap(data)
            gmaps.display(map)

Installation
------------

gmaps can only be installed from source. Clone the git repository by running::

    $ git clone https://github.com/pbugnion/gmaps.git

Change to the project's root directory and run::

    $ python setup.py install

Getting started
---------------

Currently, only heatmaps are supported. Draw a heatmap by passing a list of (latitude, longitude)
pairs to the heatmap command.

There are example notebooks in the examples directory. The heatmap example is
also visible `on nbviewer
<http://nbviewer.ipython.org/github/pbugnion/gmaps/blob/master/examples/ipy3/heatmap_demo.ipynb>`_,
but note that you need to download the notebook to actually see the Google Map.

Issue reporting and contributing
--------------------------------

Report issues using the `github issue tracker <https://github.com/pbugnion/gmaps/issues>`_.

Contributions are welcome. Read the CONTRIBUTING guide to learn how to contribute.
