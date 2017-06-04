
How to release jupyter-gmaps
----------------------------

This is a set of instructions for releasing to Pypi. The release process is somewhat automated with an `invoke <http://docs.pyinvoke.org/en/latest/getting_started.html>`_ task file. You will need `invoke` installed.

 - Run ``invoke prerelease <version>``, where ``version`` is the version number of the release candidate. If you are aiming to release version ``0.5.0``, this will be ``0.5.0-rc1``. This will automatically bump the version numbers and upload the release to Pypi and NPM. Unfortunately, Pypi does not recognize this as a pre-release, and therefore gives it more precendence than the previous, stable release. To correct this, go to the gmaps page on Pypi, then go to the `releases` tab and manually hide that release and un-hide the previous one.

 - Verify that you can install the new version and that it works correctly with ``pip install gmaps==<new version>`` and ``jupyter nbextension enable --py --sys-prefix gmaps``. It's best to verify the installation on a clean virtual machine (rather than just in a new environment) since installation is more complex than for pure Python packages.

 - If the manual installation tests failed, fix the issue and repeat the previous steps with ``rc2`` etc. If installing worked, proceed to the next steps.

 - Run ``invoke release <version>``, where ``version`` is the version number of the release (e.g. ``0.5.0``). You will be prompted to enter a changelog.

 - Verify that the new version is available by running ``pip install gmaps`` in a new virtual environment.

 - Run ``invoke postrelease <version>``, where ``version`` is the version number of the new release. This will commit the changes in version, add an annotated tag from the changelog and push the changes to Github. It will then change the version back to a ``-dev`` version.

 - Run ``invoke release_conda <version>`` to release the new version to conda-forge.
