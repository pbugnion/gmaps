
Release notes
-------------

Version 0.9.0
=============

This release:
- adds support for JupyterLab 1.0 and removes support for JupyterLab <1.0 (PRs 310 and 312).
*jupyter-gmaps* 0.8.4 was the last version to support JupyterLab <1.0.
- removes a build artifact that was committed to source control (PR 311).

Version 0.8.4
=============

This release:
- adds the ability to draw circles in the drawing layer (PR 295)
- adds JS unit testing to the build pipeline (PR 295)
- fixes deprecation warnings for obsolete traitlets code (PR 294)

Version 0.8.3
=============

This release: 

- allows dynamically updating an already constructed marker and
  symbol layer. This makes it easier to use that layer in
  widget applications (PR 285, 286).
- adds support for marker layers with no markers (PR 288)
- updates the Google JS API version form 3.31 to 3.34 (PR 289)
- updates the build process to use webpack 4 (PR 290)
- adds the return type of the marker, symbol and geojson layer
  to the factory functions (PR 291)
- autoformats the JS parts of the code with prettier (PR 279)
- adds checks on the integrity of the documentation as part 
  of the build process (PR 293).

Version 0.8.2 - 13th October 2018
=================================

This minor release fixes an issue where the fill color,
stroke color or scale were not respected when embedding
a map as HTML if they were exactly on the default value
in the Python layer (PR 276).

Version 0.8.1 - 26th September 2018
===================================

This minor release:

- adds the tilt option to maps (PR 253).
- fixes passing fill and stroke opacity attributes to heatmap (PR 263).
- fixes an issue on JupyterLab where the color of output cells was 
  changed to grey when built with jupyter-gmaps (PR 268).
- updates the release process to use twine (PR 269).

Version 0.8.0 - 22nd April 2018
===============================

This minor release:

- Changes the directions layer widget to add the `start`, `end` and `waypoints`
  traitlets. This deprecates the `data` traitlet, scheduled for removal in 0.9.0.
  (PR 236).
- The directions layer now reacts to changes in start, end and waypoints by 
  re-calculating the route (PR 239)
- The directions layer now supports styling the route (PR 247)
- Errors in the direction layer are now shown in the error box, rather than as
  an uncatchable exception (PR 242)
- Errors authenticating result in an error message that replaces the map,
  rather than the cryptic 'Oops, something went wrong' default that Google Maps
  provides (PR 240)
- Adds style to error box (PR 243)
- Removes the deprecated `data` traitlet from the Heatmap and WeightedHeatmap
  widgets. See PR 249 for a migration pathway. (PR 249)
- Introduces the Opacity traitlet for encoding stroke and fill opacities (PR 248)

Version 0.7.4 - 5th April 2018
==============================

This minor release:
 - allows setting which map type we use (PR 232)
 - allows setting how the map interacts with the webpage, in terms of capturing scroll events (PR 232)
 - allows setting the style of polygons on the drawing layer (PR 229)
 - fixes a bug that stopped the drawing layer from being downloadable as a PNG (PR 227)

Version 0.7.3 - 11th March 2018
===============================

This release:

- simplifies setting the width and height for a figure. We now do
  not need to explicitly set the width and height of the embedded
  map (PR 221).
- allows customising the style of lines added to the map in the
  drawing layer (PR 225).

Version 0.7.2 - 16th February 2018
==================================

This release adds support for JupyterLab (PR 218).

Version 0.7.1 - 10th February 2018
==================================

This minor release:

 - Deprecates the `.data` traitlet in heatmaps and weighted heatmaps in favour
   of `.locations` (for heatmap) and `.locations` and `.weights`. These now have
   validation, so a user can pass in a dataframe or numpy array (PR 211).
 - React to changes in the new `.locations` and `.weights` traitlets to actually
   update heatmaps dynamically. (PR 212).
 - Reduces page load size in documentation by compressing the images (PR 217).

Version 0.7.0 - 11th November 2017
==================================

- This minor release adds a drawing layer, giving the user the ability
  to add arbitrary lines, markers and polygons to a map. The developer
  can bind callbacks that are run when a feature is added, allowing
  the development of complex, widgets- based application on top of
  jupyter-gmaps (PR 183).
- It fixes a bug where the bounds were incorrectly calculated when two
  longitudes coincided (PR 204).
- It fixes a bug where, for single latitudes, the returned bounds
  could stretch beyond what Google Maps allows (PR 204)

Version 0.6.2 - 30th October 2017
=================================

This minor release:
 - fixes a bug that was introduced by shadowing a reserved traitlets method (PR 184)
 - migrates the codebase to flake8 3.5.0 (PR 195)

Version 0.6.1 - 1st September 2017
==================================

This is a patch release that is identical to 0.6.0. The dependencies in the
conda-forge release of 0.6.0 were badly specified.

Version 0.6.0 - 26th August 2017
================================

This release:
 - PRs 166, 171 and 172 migrate jupyter-gmaps to ipywidgets 7.0.0 (released on the 18th August 2017). This is a breaking change: jupyter-gmaps will not work with ipywidgets 6.x versions.
 - PRs 163 and 169 add a layer for displaying bicycling information.
 - PRs 165 and 169 add a layer for displaying transit (public transport) information.
 - PR 170 adds a layer for displaying traffic information.
 - PR 173 improves the layout of the CSS
 - PR 173 improves the CSS used for embedding

Version 0.5.4 - 15th July 2017
==============================

This release:
 - Fixes a bug where bounds were incorrectly calculated for the case where there was a single point in the data (PR 160).
 - Allows setting the travel mode in the directions layer (PR 157).
 - Fixes the release script to use a fork of the conda-forge feedstock (PR 156).

Version 0.5.3 - 8th July 2017
=============================

This release adds two minor features:
 - The directions layer can be customised, in particular how the route is calculated ([PR 153](https://github.com/pbugnion/gmaps/pull/153))
 - The user can explicitly set the map zoom and center ([PR 154](https://github.com/pbugnion/gmaps/pull/154))

It also makes the following non-breaking changes:
 - Refactor JS to use ES6 classes.

Version 0.5.2 - 25th June 2017
==============================

This is a bugfix release.
 - Bounds are now calculated correctly when there are multiple layers (PR 148).
 - Latitude bounds cannot exceed the maximum allowed by Google Maps (PR 149).
 - Alpha values of 1.0 are now allowed.

Version 0.5.1 - 3rd June 2017
=============================

This patch release:
 - fixes flakiness downloading images as PNGs (issue 129).
 - adds an error box view for errors that come up in the frontend.

It adds improvements to the development workflow:
 - License is included in the source to facilicate deployment to conda-forge
 - Facilitate installation in dev mode.
 - Automation of release process.

Version 0.5.0 - 8th May 2017
============================

This release:

 - introduces a new Figure widget that wraps a toolbar and a map
 - adds the ability to export maps to PNG
 - fixes bugs and outdated dependencies that prevented embedding maps in
   rendered HTML.

Version 0.4.1 - 14th March 2017
===============================

 * Add a GeoJSON layer (PRs #106 and #115)
 * Add the `geojson_geometries` module for bundling GeoJSON geometries with `jupyter-gmaps` (PR #111).
 * Minor improvements to README and compatibility guide.
 * Support for Python 3.6 (PR #107).

Version 0.4.0 - 28th January 2017
=================================

 * Add factory functions to make creating layers easier. Instead of creating widgets directly, the widgets are instantiated through `*_layer()` functions which are easier to use and more tolerant of user input. This fixes:
    - passing arbitrary iterables to the factory function (issue #66)
    - passing more complex sets of options (issue #65)
 * The directions interface is now a first class layer (issue #64)
 * A regression whereby the API documentation wasn't building on readthedocs is now fixed (PR #105).

Version 0.3.6 - 28th December 2016
==================================

 * Adds info boxes to the marker and symbol layers (PR #98).

Version 0.3.5 - 8th October 2016
================================

 * Bugfix in deprecated heatmap method (PR #89).

Version 0.3.4 - 26th September 2016
===================================

 * Add marker and symbol layer (PR #78)
 * Fix bug involving incorrect latitude bound calculation.

Version 0.3.3 - 7th September 2016
==================================

 * Improve automatic bounds calculations for heatmaps (PR #84)

Version 0.3.2 - 30th July 2016
==============================

 * Allow setting heatmap options (issues #74)
 * Basic unit tests for traitlets, mixins and datasets
 * Continuous integration with Travis CI.

Version 0.3.1 - 30th July 2016
==============================

Fix release to allow injecting Google maps API keys. Google maps now mandates API keys, so this release provides a way to pass in a key (issue #61).

This release also includes a fix for having multiple layers on the same map.

Version 0.3.0 - 14th June 2016
==============================

Complete re-write of gmaps to work with IPython 4.2 and ipywidgets 5.x. This release is at feature parity with the previous release, but the interface differs:

 * Maps are now built up from a base to which we add layers.
 * Heatmaps and weighted heatmaps are now layers that can be added to the base map.
 * Add the acled_africa dataset to demonstrate heatmaps with a substantial amount of data.
 * Now fits into the Jupyter installation convention for widget extensions.
 * Add sphinx documentation
 * Remove example notebooks (these may be added back in a later release)

Version 0.2.2 - 26th March 2016
===============================

 * Remove dependency on Numpy
 * Fix broken datasets example (issue #52)

Version 0.2.1 - 26th March 2016
===============================

test release -- no changes.

Version 0.2 - 2nd January 2016
==============================

 * IPython 4.0 compatibility
 * Python 3 compatibility

 * Drop IPython 2.x compatibility

Version 0.1.6 - 8th December 2014
=================================

Fixed typo in setup script.

Version 0.1.5 - 8th December 2014
=================================

Weighted heatmaps and datasets

 * Added possibility of including weights in heatmap data.
 * Added a datasets module to allow new users to play around with data
   without having to find their own dataset.

Version 0.1.4 - 4th December 2014
=================================

Another bugfix release.

 * Fixed a bug that arose when using heatmap with default values of some of the
   parameters.

Version 0.1.3 - 4th December 2014
=================================

Bugfix release.

 * Fixed a bug that arose when using the heatmap with IPython2.3 in the
   previous release. The bug was caused by the slightly different traitlets API
   between the two IPython versions.

Version 0.1.2 - 4th December 2014
=================================

Minor heatmap improvements.

 * Exposed the 'maxIntensity' and 'radius' options for heatmaps.

Version 0.1.1 - 2nd December 2014
=================================

Bugfix release.

 * Ensures the notebook extensions are actually included in the source
   distribution.

Version 0.1 - 2nd December 2014
===============================

Initial release.

 * Allows plotting heatmaps from a list / array of pairs of longitude, latitude
   floats on top of a Google Map.
