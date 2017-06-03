
Exporting maps
--------------

Exporting to PNG
^^^^^^^^^^^^^^^^

You can save maps to PNG by clicking the `Download` button in the toolbar.
This will download a static copy of the map.

This feature suffers from some know issues:

 - there is no way to set the quality of the rendering at present,
 - you cannot export maps that contain a `Directions` layer (see `the issue <https://github.com/pbugnion/gmaps/issues/144>`_ on Github for details).


Exporting to HTML
^^^^^^^^^^^^^^^^^

You can export maps to HTML using the infrastructure provided by `ipywidgets`. In the menu of your notebook, click `Widgets` > `Embed widgets`. This will open a modal containing some HTML. The HTML is composed of several script tags:

.. code-block:: html

  <!-- Script tags that need to go into the head of the document -->
  <script src="https://unpkg.com/jupyter-js-widgets@~2.1.4/dist/embed.js"></script>

  <script type="application/vnd.jupyter.widget-state+json">
      // State of the widgets
  </script>

  <!--
      Script tags that should be embedded where the views should go.
      There should be one tag per cell containing a widget
  -->
  <script type="application/vnd.jupyter.widget-view+json">
    {
    "model_id": "c05e9b0ca0dd405295d2adde29776c95"
    }
  </script>
  <script type="application/vnd.jupyter.widget-view+json">
    {
    "model_id": "ea6c1d9f7d1c4065818fafa1ed9125aa"
    }
  </script>
    

The first two define the state of the widgets and should be embedded in the head of the HTML document. The remaining tags describe the views. There will be one for each cell containing a widget in the notebook. You should paste these into the DOM elements that need to hold the views.

Additionally, you will need to import `jupyter-gmaps`, JQuery and the Bootstrap CSS in the head of your HTML document. You can use this template to make sure you have all the imports:

.. code-block:: html

    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
            <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>

            {{ paste first two script tags here }}

        </head>
        <body>
            <div>
                {{ paste script tags defining the views here }}
            </div>
        </body>
    </html>

    
Thus, a valid HTML document containing a single map would look like this (the API key has been redacted, but apart from that, this will work out of the box):

.. code-block:: html

   <html>
       <head>
           <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
           <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>

           <script src="https://unpkg.com/jupyter-js-widgets@~2.1.4/dist/embed.js"></script>
           <script type="application/vnd.jupyter.widget-state+json">
           {
               "version_major": 1,
               "version_minor": 0,
               "state": {
                   "acd855c3e79c4100bf23ac682b97fef6": {
                       "model_name": "LayoutModel",
                       "model_module": "jupyter-js-widgets",
                       "model_module_version": "~2.1.4",
                       "state": {
                           "_model_module_version": "~2.1.4",
                           "height": "400px",
                           "_view_module_version": "~2.1.4",
                           "align_self": "stretch"
                       }
                   },
                   "e6333a5e4408424fa1d13bafe32e3ec8": {
                       "model_name": "PlainmapModel",
                       "model_module": "jupyter-gmaps",
                       "model_module_version": "*",
                       "state": {
                           "layers": [],
                           "_dom_classes": [],
                           "msg_throttle": 1,
                           "_model_module_version": "*",
                           "_view_module_version": "*",
                           "data_bounds": [
                               [
                                   46.2,
                                   6.1
                               ],
                               [
                                   47.2,
                                   7.1
                               ]
                           ],
                           "layout": "IPY_MODEL_acd855c3e79c4100bf23ac682b97fef6",
                           "configuration": {
                               "api_key": "AIza_FILL_ME_IN"
                           }
                       }
                   }
               }
           }
           </script>

       </head>

       <body>
           <h1>GMaps embedding example</h1>
           <div id="widget-embedded-here">
               <script type="application/vnd.jupyter.widget-view+json">
               {
                   "model_id": "e6333a5e4408424fa1d13bafe32e3ec8"
               }
               </script>
           </div>
       </body>
   </html>


