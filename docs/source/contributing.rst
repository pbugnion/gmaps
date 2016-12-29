
Contributing to jupyter-gmaps
=============================

Contributions are welcome! If you're not sure how to get started, or want to run some ideas past the committers, open an issue through the `Github issue tracker <https://github.com/pbugnion/gmaps/issues>`.

How to release jupyter-gmaps
----------------------------

This is a set of instructions for releasing to Pypi.

 - Append the suffix ``rc1`` to the version in ``_version.py`` 

 - Upload the pre-release to Pypi with ``python setup.py sdist upload``. Unfortunately, Pypi does not recognize this as a pre-release, and therefore gives it more precendence than the previous, stable release. To correct this, go to the gmaps page on Pypi, then go to the `releases` tab and manually hide that release and un-hide the previous one.

 - Verify that you can install the new version and that it works correctly with ``pip install gmaps==<new version>`` and ``jupyter nbextension enable --py --sys-prefix widgetsnbextension``. It's best to verify the installation on a clean virtual machine (rather than just in a new environment) since installation is more complex than for pure Python packages.

 - If the manual installation tests failed, fix the issue and repeat the previous steps with ``rc2`` etc. If installing worked, proceed to the next steps.

 - Write the changelog for the new version and commit the changes.

 - Bump the version number in ``_version.py`` to a stable version (e.g. 0.3.6).

 - Bump the version number in ``docs/source/conf.py`` for both the ``version`` and the ``release`` variables.

 - Bump the version number in ``js/package.json``.

 - Run ``python setup.py sdist bdist upload`` to upload the artefact to pypi.

 - Verify that the new version is available by running ``pip install gmaps`` in a new virtual environment.

 - Commit the changes in version.

 - Tag the new version with an annotated tag, e.g. ``git tag -a v0.3.6``. Include a ``v`` in front of the version number. Copy the release notes as the tag annotation.

 - Push the new commits and the tag with ``git push origin master --tags``

 - Change the version number in ``_version.py`` back to a ``dev`` version. It's better to bump just the patch release, even if you think the next release may be a minor release.

 - Commit the change with a message like `Back to dev`.

 - Push the change to master.
