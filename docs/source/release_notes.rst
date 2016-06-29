
Release notes
-------------

Version 0.3.1
=============

Fix release to allow injecting Google maps API keys. Google maps now mandates API keys, so this release provides a way to pass in a key (issue #61).

This release also includes a fix for having multiple layers on the same map.

Version 0.3.0
=============

Complete re-write of gmaps to work with IPython 4.2 and ipywidgets 5.x. This release is at feature parity with the previous release, but the interface differs:

 * Maps are now built up from a base to which we add layers.
 * Heatmaps and weighted heatmaps are now layers that can be added to the base map.
 * Add the acled_africa dataset to demonstrate heatmaps with a substantial amount of data.
 * Now fits into the Jupyter installation convention for widget extensions.
 * Add sphinx documentation
 * Remove example notebooks (these may be added back in a later release)

Version 0.2.2
=============

 * Remove dependency on Numpy
 * Fix broken datasets example (issue #52)

Version 0.2.1
=============

test release -- no changes.

Version 0.2
===========

 * IPython 4.0 compatibility
 * Python 3 compatibility

 * Drop IPython 2.x compatibility

Version 0.1.6
=============

Fixed typo in setup script.

Version 0.1.5
=============

Weighted heatmaps and datasets

 * Added possibility of including weights in heatmap data.
 * Added a datasets module to allow new users to play around with data
   without having to find their own dataset.

Version 0.1.4
=============

Another bugfix release.

 * Fixed a bug that arose when using heatmap with default values of some of the
   parameters.

Version 0.1.3
=============

Bugfix release.

 * Fixed a bug that arose when using the heatmap with IPython2.3 in the
   previous release. The bug was caused by the slightly different traitlets API
   between the two IPython versions.

Version 0.1.2
=============

Minor heatmap improvements.

 * Exposed the 'maxIntensity' and 'radius' options for heatmaps.

Version 0.1.1
=============

Bugfix release.

 * Ensures the notebook extensions are actually included in the source
   distribution.

Version 0.1
===========

Initial release.

 * Allows plotting heatmaps from a list / array of pairs of longitude, latitude
   floats on top of a Google Map.
