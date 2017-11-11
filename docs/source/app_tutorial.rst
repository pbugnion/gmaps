
Building applications with `jupyter-gmaps`
------------------------------------------

You can use `jupyter-gmaps` as a component in a `Jupyter widgets <https://ipywidgets.readthedocs.io/en/stable/>`_ application. Jupyter widgets let you embed rich user interfaces in Jupyter notebooks. For instance:
 - you can use maps as a way to get user input. The drawing layer lets users draw markers, lines or polygons on the map. We can specify arbitrary Python code that runs whenever a shape is added to the map. As an example, we will build an application where, whenever the user places a marker, we retrieve the address of the marker and write it in a text widget. 
 - you can use maps as a way to display the result of an external computation. For instance, if you have timestamped geographical data (for instance, you have the date and coordinates of a series of events), you can combine a heatmap with a slider to see how events unfold over time.

.. _reacting-to-user-actions:

Reacting to user actions on the map
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The drawing layer lets us specify Python code to be executed whenever the user
adds a feature (like a marker, a line or a polygon) to the map. To demonstrate
this, we will build a small application for *reverse geocoding*: when the user
places a marker on the map, we will find the address closest to that marker and
write it in a `text widget
<https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#Text>`_.
We will use `geopy <https://pypi.python.org/pypi/geopy>`_, a wrapper around
several geocoding APIs, to calculate the address from the marker's coordinates.

This is the entire code listing::

  from tabulate import tabulate
  import ipywidgets as widgets
  import geopy
  import gmaps

  API_KEY = 'AIz...'

  gmaps.configure(api_key=API_KEY)

  class ReverseGeocoder(object):
      """
      Jupyter widget for finding addresses.

      The user places markers on a map. For each marker,
      we use `geopy` to find the nearest address to that
      marker, and write that address in a text box.
      """

      def __init__(self):
          self._figure = gmaps.figure()
          self._drawing = gmaps.drawing_layer()
          self._drawing.on_new_feature(self._new_feature_callback)
          self._figure.add_layer(self._drawing)
          self._address_box = widgets.Text(
              description='Address: ',
              disabled=True,
              layout={'width': '95%', 'margin': '10px 0 0 0'}
          )
          self._geocoder = geopy.geocoders.GoogleV3(api_key=API_KEY)
          self._container = widgets.VBox([self._figure, self._address_box])

      def _get_location_details(self, location):
          return self._geocoder.reverse(location, exactly_one=True)

      def _clear_address_box(self):
          self._address_box.value = ''

      def _show_address(self, location):
          location_details = self._get_location_details(location)
          if location_details is None:
              self._address_box.value = 'No address found'
          else:
              self._address_box.value = location_details.address

      def _new_feature_callback(self, feature):
          try:
              location = feature.location
          except AttributeError:
              return # Not a marker

          # Clear address box to signify to the user that something is happening
          self._clear_address_box()

          # Remove all markers other than the one that has just been added.
          self._drawing.features = [feature]

          # Compute the address and display it
          self._show_address(location)

      def render(self):
          return self._container

  ReverseGeocoder().render()

There are several things to note on this:

- We wrap the application in a ``ReverseGeocoder`` class. Wrapping your
  application in a class (rather than using the notebook's global namespace)
  helps with encapsulation and lets you instantiate this widget multiple times.
  Since the flow through widget applications is often more complex than linear
  data analysis workflows, encapsulation will improve your ability to reason
  about the code.
- As part of the class constructor, we use :func:`gmaps.figure` to create a
  figure. We add use :func:`gmaps.drawing_layer` to create a drawing layer,
  which we add to the figure. We also create a ``widgets.Text`` widget. This is
  a text box in which we will write the address. We then wrap our figure and the
  text box in a single ``widgets.VBox``, a widget container that stacks widgets
  vertically.
- We register a callback on the drawing layer using ``.on_new_feature``. The
  function that we pass in to ``.on_new_feature`` will get called whenever the
  user adds a feature to the map. This is the hook that lets us build complex
  applications on top of the drawing layer: we can run arbitrary Python code
  when the user adds a marker to the map.
- In the ``.on_new_feature`` callback, we first check whether the feature that
  has been added is a marker (the user could, in principle, have added another
  feature type, like a line, to the map).
- Assuming the feature is a valid marker, we first clear the text widget
  containing the address. This gives feedback to the user that something is
  happening.
- We then re-write the ``.features`` array of the drawing layer, keeping just
  the marker that the user has just added. This clears previous markers,
  avoiding clutter on the map.
- We then use `geopy <https://pypi.python.org/pypi/geopy>`_ to find the
  adddress. Assuming the address is valid, display it in the text widget.
