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
