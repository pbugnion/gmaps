
Contributing
============

We want to start by thanking you for using Jupyter-gmaps. We very much appreciate all of the users who catch bugs, contribute enhancements and features or add to the documentation. Every contribution is meaningful, so thank you for participating.

How to contribute
-----------------

Code contributions are more than welcome. Take a look at the `issue tracker <https://github.com/pbugnion/gmaps/issues>`_, specially issues labelled as `beginner-friendly`. These are issues which have a lot of impact on the project, but don't require understanding the entire codebase.

Beyond code, the following contributions will make `gmaps` a better project:

 - additional datasets related to geographical data. The data needs to be clean, of reasonable size (ideally not more than 1MB), and should be clearly related to geography.
 - additional GeoJSON geometries. These should be clean and reasonably small (ideally 1-3MB).
 - Examples of you using Jupyter-gmaps. If you've used gmaps and have an artefact to show for it (a blogpost or an image), I'm very happy to put a link in the documentation.


Installing a development version of gmaps
-----------------------------------------

See the `installation instructions
<http://jupyter-gmaps.readthedocs.io/en/latest/install.html#development-version>`_
for installing a development version.

Testing
-------

We use nose for unit testing. Run ``nosetests`` in the root directory of the project to run all the tests,
or in a specific directory to just run the tests in that directory.

Guidelines
----------

Workflow
^^^^^^^^

We loosely follow the `git workflow <http://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html>`_ used in numpy development.  Features should
be developed in separate branches and merged into the master branch when
complete.

Code
^^^^

Please follow the `PEP8 conventions <http://www.python.org/dev/peps/pep-0008/>`_ for formatting and indenting code and for variable names.

