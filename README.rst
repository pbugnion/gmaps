.. Automatically generated from LONG_DESCRIPTION keyword in 
.. setup.py. Do not edit directly.

gmaps
=====

gmaps is a plugin for including interactive Google maps in the IPython Notebook.

Let's plot a heatmap (data taken from the `Google maps API documentation <https://developers.google.com/maps/documentation/javascript/heatmaplayer>`_):

::

    In [1]: import gmaps
            gmaps.init()

    In [2]: data = [ [ 37.782, -122.447 ], # [ latitude, longitude ] pairs
                     [ 37.782, -122.445 ],
                     [ 37.782, -122.443 ],
                     [ 37.782, -122.441 ],
                     [ 37.782, -122.439 ],
                     [ 37.782, -122.437 ] ]
            map = gmaps.heatmap(data)
            gmaps.display(map)

Installation
------------

gmaps can only be installed from source. Clone the git repository by running::

    $ git clone https://github.com/pbugnion/gmaps.git

Change to the project's root directory and run::

    $ pip install -e "."

Getting started
---------------

Before running any `gmaps` code, you must call ``gmaps.init()``. It must be the last line
in its IPython cell.

Currently, only heatmaps are supported. Draw a heatmap by passing a list of (latitude, longitude)
pairs to the heatmap command.

Issue reporting and contributing
--------------------------------

Report issues using the `github issue tracker <https://github.com/pbugnion/gmaps/issues>`_.

Contributions are welcome. Read the CONTRIBUTING guide to learn how to contribute.
