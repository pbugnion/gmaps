
Release notes
-------------

Version 0.7.0
=============

- This minor release adds a drawing layer, giving the user the ability to add
arbitrary lines, markers and polygons to a map. The developer can bind callbacks
that are run when a feature is added, allowing the development of complex, widgets-
based application on top of jupyter-gmaps (PR 183).
- It fixes a bug where the bounds were incorrectly calculated when two longitudes coincided (PR 204).
- It fixes a bug where, for single latitudes, the returned bounds could stretch beyond what Google Maps allows (PR 204)

Version 0.6.2
=============

This minor release:
 - fixes a bug that was introduced by shadowing a reserved traitlets method (PR 184)
 - migrates the codebase to flake8 3.5.0 (PR 195)

Version 0.6.1
=============

This is a patch release that is identical to 0.6.0. The dependencies in the
conda-forge release of 0.6.0 were badly specified.

Version 0.6.0
=============

This release:
 - PRs 166, 171 and 172 migrate jupyter-gmaps to ipywidgets 7.0.0 (released on the 18th August 2017). This is a breaking change: jupyter-gmaps will not work with ipywidgets 6.x versions.
 - PRs 163 and 169 add a layer for displaying bicycling information.
 - PRs 165 and 169 add a layer for displaying transit (public transport) information.
 - PR 170 adds a layer for displaying traffic information.
 - PR 173 improves the layout of the CSS
 - PR 173 improves the CSS used for embedding

Version 0.5.4
=============

This release:
 - Fixes a bug where bounds were incorrectly calculated for the case where there was a single point in the data (PR 160).
 - Allows setting the travel mode in the directions layer (PR 157).
 - Fixes the release script to use a fork of the conda-forge feedstock (PR 156).

Version 0.5.3
=============

This release adds two minor features:
 - The directions layer can be customised, in particular how the route is calculated ([PR 153](https://github.com/pbugnion/gmaps/pull/153))
 - The user can explicitly set the map zoom and center ([PR 154](https://github.com/pbugnion/gmaps/pull/154))

It also makes the following non-breaking changes:
 - Refactor JS to use ES6 classes.

Version 0.5.3
=============

This release adds two minor features:
 - The directions layer can be customised, in particular how the route is calculated ([PR 153](https://github.com/pbugnion/gmaps/pull/153))
 - The user can explicitly set the map zoom and center ([PR 154](https://github.com/pbugnion/gmaps/pull/154))

It also makes the following non-breaking changes:
 - Refactor JS to use ES6 classes.

Version 0.5.2
=============

This is a bugfix release.
 - Bounds are now calculated correctly when there are multiple layers (PR 148).
 - Latitude bounds cannot exceed the maximum allowed by Google Maps (PR 149).
 - Alpha values of 1.0 are now allowed.

Version 0.5.1
=============

This patch release:
 - fixes flakiness downloading images as PNGs (issue 129).
 - adds an error box view for errors that come up in the frontend.

It adds improvements to the development workflow:
 - License is included in the source to facilicate deployment to conda-forge
 - Facilitate installation in dev mode.
 - Automation of release process.

Version 0.5.0
=============

This release:

 - introduces a new Figure widget that wraps a toolbar and a map
 - adds the ability to export maps to PNG
 - fixes bugs and outdated dependencies that prevented embedding maps in
   rendered HTML.

Version 0.4.1
=============

 * Add a GeoJSON layer (PRs #106 and #115)
 * Add the `geojson_geometries` module for bundling GeoJSON geometries with `jupyter-gmaps` (PR #111).
 * Minor improvements to README and compatibility guide.
 * Support for Python 3.6 (PR #107).

Version 0.4.0
=============

 * Add factory functions to make creating layers easier. Instead of creating widgets directly, the widgets are instantiated through `*_layer()` functions which are easier to use and more tolerant of user input. This fixes:
    - passing arbitrary iterables to the factory function (issue #66)
    - passing more complex sets of options (issue #65)
 * The directions interface is now a first class layer (issue #64)
 * A regression whereby the API documentation wasn't building on readthedocs is now fixed (PR #105).

Version 0.3.6
=============

 * Adds info boxes to the marker and symbol layers (PR #98).

Version 0.3.5
=============

 * Bugfix in deprecated heatmap method (PR #89).

Version 0.3.4
=============

 * Add marker and symbol layer (PR #78)
 * Fix bug involving incorrect latitude bound calculation.

Version 0.3.3
=============

 * Improve automatic bounds calculations for heatmaps (PR #84)

Version 0.3.2
=============

 * Allow setting heatmap options (issues #74)
 * Basic unit tests for traitlets, mixins and datasets
 * Continuous integration with Travis CI.

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
