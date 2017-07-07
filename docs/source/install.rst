
Installation
------------

Installing `gmaps` with `conda`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way to install `gmaps` is with `conda`::

    $ conda install -c conda-forge gmaps

Installing `gmaps` with `pip`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do not use conda, you can install `gmaps` with pip. The current version
of `gmaps` is only tested with *IPython 4.2* or later and *ipywidgets 6.0.0* or
later. To upgrade to the latest versions, use::

    $ pip install -U jupyter

Make sure that you have enabled widgets extensions to Jupyter::

    $ jupyter nbextension enable --py --sys-prefix widgetsnbextension

You can then install gmaps with::

    $ pip install gmaps

Then tell Jupyter to load the extension with::

    $ jupyter nbextension enable --py --sys-prefix gmaps

Development version
^^^^^^^^^^^^^^^^^^^

You must have `NPM <https://www.npmjs.com>`_ to install the development version. You can install NPM with your package manager.

We strongly recommend installing `jupyter-gmaps` in a virtual environment (either a conda environment or a virtualenv environment).

Clone the git repository by running::

    $ git clone https://github.com/pbugnion/gmaps.git

For the initial installation, run::

    $ ./dev-install

This installs ``gmaps`` in editable mode and installs the Javascript components as symlinks.

If you then make changes to the code, you can make those changes available to a running notebook server by:

 - restarting the kernel if you have made changes to the Python source code
 - running ``npm run update`` in the ``js/`` directory and `refreshing` the browser page containing the notebook if you have made changes to the JavaScript source. You do not need to restart the kernel.
 - running ``npm run update``, refreshing the browser and restarting the kernel if you have made changes to both the Python and JavaScript source.

You should not need to restart the notebook server.

Source code
^^^^^^^^^^^

The `jupyter-gmaps` source is available on `GitHub <https://github.com/pbugnion/gmaps>`_.
