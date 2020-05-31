|travis| |pypi| |docs|

gmaps
=====

gmaps is a plugin for including interactive Google maps in the IPython Notebook.

Let's plot a `heatmap <http://jupyter-gmaps.readthedocs.io/en/latest/tutorial.html#heatmaps>`_ of taxi pickups in San Francisco:

.. code:: python

    import gmaps
    import gmaps.datasets
    gmaps.configure(api_key="AI...") # Your Google API key

    # load a Numpy array of (latitude, longitude) pairs
    locations = gmaps.datasets.load_dataset("taxi_rides")

    fig = gmaps.figure()
    fig.add_layer(gmaps.heatmap_layer(locations))
    fig

.. image:: docs/source/_images/taxi_example.png

We can also plot chloropleth maps using `GeoJSON <http://jupyter-gmaps.readthedocs.io/en/latest/tutorial.html#geojson-layer>`_:

.. code:: python

    from matplotlib.cm import viridis
    from matplotlib.colors import to_hex

    import gmaps
    import gmaps.datasets
    import gmaps.geojson_geometries

    gmaps.configure(api_key="AI...") # Your Google API key

    countries_geojson = gmaps.geojson_geometries.load_geometry('countries') # Load GeoJSON of countries

    rows = gmaps.datasets.load_dataset('gini') # 'rows' is a list of tuples
    country2gini = dict(rows) # dictionary mapping 'country' -> gini coefficient
    min_gini = min(country2gini.values())
    max_gini = max(country2gini.values())
    gini_range = max_gini - min_gini

    def calculate_color(gini):
        """
        Convert the GINI coefficient to a color
        """
        # make gini a number between 0 and 1
        normalized_gini = (gini - min_gini) / gini_range

        # invert gini so that high inequality gives dark color
        inverse_gini = 1.0 - normalized_gini

        # transform the gini coefficient to a matplotlib color
        mpl_color = viridis(inverse_gini)

        # transform from a matplotlib color to a valid CSS color
        gmaps_color = to_hex(mpl_color, keep_alpha=False)

        return gmaps_color

    # Calculate a color for each GeoJSON feature
    colors = []
    for feature in countries_geojson['features']:
        country_name = feature['properties']['name']
        try:
            gini = country2gini[country_name]
            color = calculate_color(gini)
        except KeyError:
            # no GINI for that country: return default color
            color = (0, 0, 0, 0.3)
        colors.append(color)

    fig = gmaps.figure()
    gini_layer = gmaps.geojson_layer(
        countries_geojson,
        fill_color=colors,
        stroke_color=colors,
        fill_opacity=0.8)
    fig.add_layer(gini_layer)
    fig

.. image:: docs/source/_images/geojson-2.png

Or, for coffee fans, a map of all Starbucks in the UK:

.. code:: python

    import gmaps
    import gmaps.datasets
    gmaps.configure(api_key="AI...") # Your Google API key

    df = gmaps.datasets.load_dataset_as_df('starbucks_kfc_uk')

    starbucks_df = df[df['chain_name'] == 'starbucks']
    starbucks_df = starbucks_df[['latitude', 'longitude']]

    starbucks_layer = gmaps.symbol_layer(
	starbucks_df, fill_color="green", stroke_color="green", scale=2
    )
    fig = gmaps.figure()
    fig.add_layer(starbucks_layer)
    fig


.. image:: docs/source/_images/starbucks-symbols.png


Installation
------------

Installing `jupyter-gmaps` with `conda`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way to install `gmaps` is with `conda`::

    $ conda install -c conda-forge gmaps

Installing `jupyter-gmaps` with `pip`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure that you have enabled `ipywidgets` widgets extensions::

    $ jupyter nbextension enable --py --sys-prefix widgetsnbextension

You can then install gmaps with::

    $ pip install gmaps

Then tell Jupyter to load the extension with::

    $ jupyter nbextension enable --py --sys-prefix gmaps


Installing `jupyter-gmaps` for JupyterLab
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use `jupyter-gmaps` with JupyterLab, you will need to install the jupyter
widgets extension for JupyterLab::

    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager

You can then install `jupyter-gmaps` via pip (or conda)::

    $ pip install gmaps

Next time you open JupyterLab, you will be prompted to rebuild JupyterLab: this
is necessary to include the `jupyter-gmaps` frontend code into your JupyterLab
installation. You can also trigger this directly on the command line with::

    $ jupyter lab build

Support for JupyterLab pre 1.0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install `jupyter-gmaps` with versions of JupyterLab pre 1.0, you will need to pin the version of `jupyterlab-manager` and of `jupyter-gmaps`. Find the version of the `jupyterlab-manager` that you need from `this compatibility table <https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager>`_. For instance, for JupyterLab 0.35.x::

    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38

Then, install a pinned version of `jupyter-gmaps`::

    $ pip install gmaps==0.8.4

You will then need to rebuild JupyterLab with::

    $ jupyter lab build


Google API keys
---------------

To access Google maps, `gmaps` needs a Google API key. This key tells Google who you are, presumably so it can keep track of rate limits and such things. To create an API key, follow the instructions in the `documentation <http://jupyter-gmaps.readthedocs.io/en/latest/authentication.html>`_. Once you have an API key, pass it to `gmaps` before creating widgets (still following the instructions in the documentation). If you get a "this page can't load Google maps correctly" error, review the tips provided at the webpage linked from the "do you own this website" text provided in the error message; for example, you may not have properly configured billing for the GCP project associated with the API. 

Documentation
-------------

Documentation for `gmaps` is available `here <http://jupyter-gmaps.readthedocs.io/en/latest/>`_.

Similar libraries
-----------------

The current version of this library is inspired by the `ipyleaflet <https://github.com/ellisonbg/ipyleaflet>`_ notebook widget extension. This extension aims to provide much of the same functionality as `gmaps`, but for `leaflet maps`, not `Google maps`.

Vision and roadmap
------------------

Jupyter-gmaps is built for data scientists. Data scientists should be able to visualize geographical data on a map with minimal friction. Beyond just visualization, they should be able to integrate gmaps into their widgets so they can build interactive applications.

We see the priorities of gmaps as:

- responding to events, like user clicks, so that maps can be used interactively.
- adding greater flexibility and customisability (e.g. choosing map styles)


Issue reporting and contributing
--------------------------------

Report issues using the `github issue tracker <https://github.com/pbugnion/gmaps/issues>`_.

Contributions are welcome. Read the CONTRIBUTING guide to learn how to contribute.

.. |travis| image:: https://travis-ci.org/pbugnion/gmaps.svg?branch=master
    :target: https://travis-ci.org/pbugnion/gmaps
    :alt: Travis build status

.. |pypi| image:: https://img.shields.io/pypi/v/gmaps.svg?style=flat-square&label=version
    :target: https://pypi.python.org/pypi/gmaps
    :alt: Latest version released on PyPi

.. |docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
    :target: http://jupyter-gmaps.readthedocs.io/en/latest/
    :alt: Latest documentation
