gmaps
=====

gmaps is a plugin for including interactive Google maps in the IPython Notebook.

Let's plot a heatmap of taxi pickups in San Francisco:

::

    In [1]: import gmaps 
            import gmaps.datasets

    # load a Numpy array of (latitude, longitude) pairs
    In [2]: data = gmaps.datasets.load_dataset('taxi_rides')

    In [3]: m = gmaps.Map()
            m.add_layer(gmaps.Heatmap(data=data))
            m

.. image:: docs/example.png

Installation
------------

Dependencies
^^^^^^^^^^^^

The current version of `gmaps` is only tested with *IPython 4.2* or later and *ipywidgets 5.1.3* or later. To upgrade to the latest versions, use::

    $ pip install -U jupyter

Make sure that you have enabled widgets extensions to Jupyter::

    $ jupyter nbextension enable --py --sys-prefix widgetsnbextension

Installing `gmaps`
^^^^^^^^^^^^^^^^^^

Install the Python component using::

    $ pip install gmaps

Then tell Jupyter to load the extension with::

    $ jupyter nbextension enable --py gmaps

Development version
^^^^^^^^^^^^^^^^^^^

You must have `NPM <https://www.npmjs.com>`_ to install the development version. You can install NPM with your package manager.

You must also install ``gmaps`` in a virtual environment (or, at least, you must be able to run ``pip`` without root access).

Clone the git repository by running::

    $ git clone https://github.com/pbugnion/gmaps.git

Change to the project's root directory and run::

    $ pip install -e .

This will create a directory called ``static/`` in the ``gmaps/`` directory. This directory contains Javascript sources. Every time you change the Javascript sources, you will need to recompile this directory by re-running this command (despite everying being installed in `editable` mode). 

You can then enable the extension in Jupyter::

    $ jupyter nbextension install --py --symlink --user gmaps
    $ jupyter nbextension enable --py --user gmaps


Documentation
-------------

Documentation for `gmaps` is available `here <http://jupyter-gmaps.readthedocs.io/en/latest/>`_.

Similar libraries
-----------------

The current version of this library is inspired by the `ipyleaflet <https://github.com/ellisonbg/ipyleaflet>`_ notebook widget extension. This extension aims to provide much of the same functionality as `gmaps`, but for `leaflet maps`, not `Google maps`.


Issue reporting and contributing
--------------------------------

Report issues using the `github issue tracker <https://github.com/pbugnion/gmaps/issues>`_.

Contributions are welcome. Read the CONTRIBUTING guide to learn how to contribute.
