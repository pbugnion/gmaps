
Contributing
============

gmaps is a very new project, so there is a lot of scope for developers to make
a strong impact by contributing code, documentation and expertise. All
contributions are welcome.

How to contribute
-----------------

The `documentation <http://docs.scipy.org/doc/numpy/dev/gitwash/index.html>`_ for Numpy gives a detailed description of how to contribute to Numpy. Most of this information applies to development for ``gmaps``.

Developing with git
^^^^^^^^^^^^^^^^^^^^

You will need the `Git version control system <http://git-scm.com>`_ and an account on `Github <https://github.com>`_ to
contribute to gmaps.

1. Fork the `project repository <http://github.com/pbugnion/gmaps>`_ by clicking `Fork` in the top right of the page. This will create a copy of the fork under your account on Github.

2. Clone the repository to your computer::
   
    $ git clone https://github.com/pbugnion/gmaps.git

3. Install gmaps by running::

    $ python setup.py install_data
    $ python setup.py develop

   in the package's root directory. Passing the ``develop`` argument to
   ``setup.py``, rather than ``install``, means that python files are 
   sym-linked to the relevant ``site-packages`` directory, rather than copied.
   That means that you don't have to re-install the package when you 
   make changes to the source code. If you change the Javascript files, you
   need to re-run ``$ python setup.py install_data``.


You can now make changes and contribute them back to the source code:

1. Create a branch to hold your changes::

    $ git checkout -b my-feature

   and start making changes.

2. Work on your local copy. When you are satisfied with the changes, commit
   them to your local repository::

    $ git add 'FILES THAT YOU MODIFIED'
    $ git commit

   You will be asked to write a commit message. Explain the reasoning behind
   the changes that you made.

3. Propagate the changes back to your github account::

    $ git push -u origin my-feature

4. To integrate the changes into the main code repository, click `Pull Request`
   on the `gmaps` repository page on your accont. This will notify the
   committers who will review your code.

Updating your repository
^^^^^^^^^^^^^^^^^^^^^^^^

To keep your private repository updated, you should add the main repository as 
a remote::
    
    $ git remote add upstream git://github.com/pbugnion/gmaps.git

To update your private repository, you can then fetch new commits from
upstream::

    $ git fetch upstream
    $ git rebase upstream/master


Testing
^^^^^^^

We use nose for unit testing. Run ``nose`` in the root directory of the project to run all the tests,
or in a specific directory to just run the tests in that directory.

Guidelines
----------

Workflow
^^^^^^^^

We loosely follow the `git workflow <http://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html>`_ used in numpy development.  Features should
be developed in separate branches and merged into the master branch when
complete. Avoid putting new commits directly in your ``master`` branch.


Code
^^^^

Please follow the `PEP8 conventions <http://www.python.org/dev/peps/pep-0008/>`_ for formatting and indenting code and for variable names.


Contribution ideas
------------------

I will be very happy to accept contributions for new layers. I think that the ability to add points to the map (markers, for instance) and to plot GeoJSON would be tremendously useful.

The ability to export the maps to HTML would also be tremendously useful.

