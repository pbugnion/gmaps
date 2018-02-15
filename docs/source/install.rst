
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
 - running ``npm run build:nbextension`` in the ``js/`` directory and `refreshing` the browser page containing the notebook if you have made changes to the JavaScript source. You do not need to restart the kernel. If you are making many changes to the JavaScript directory, you can run ``npm run build:watch`` to rebuild on every change.

You should not need to restart the notebook server.

Source code
^^^^^^^^^^^

The `jupyter-gmaps` source is available on `GitHub <https://github.com/pbugnion/gmaps>`_.
