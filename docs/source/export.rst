
Exporting maps
--------------

Exporting to PNG
^^^^^^^^^^^^^^^^

You can save maps to PNG by clicking the `Download` button in the toolbar.
This will download a static copy of the map.

This feature suffers from some know issues:

 - there is no way to set the quality of the rendering at present,
 - on Google Chrome, if you pan or zoom into the map, it will fail to render,
 - on older versions of Safari, the map opens in the same window instead of downloading.


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

Additionally, you will need to import `jupyter-gmaps`, as well as JQuery, in the head of your HTML document. You can use this template to make sure you have all the imports:

.. code-block:: html

    <html>
        <head>
            <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
            <script src="https://unpkg.com/jupyter-gmaps@*/dist/index.js"></script>

            {{ paste first two script tags here }}

        </head>
        <body>
            <div>
                {{ paste script tags defining the views here }}
            </div>
        </body>
    </html>

    
Thus, a valid HTML document containing a single map would look like:

.. code-block:: html

   <html>
       <head>
           <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
           <script src="https://unpkg.com/jupyter-gmaps@*/dist/index.js"></script>

           <script src="https://unpkg.com/jupyter-js-widgets@~2.1.4/dist/embed.js"></script>
           <script type="application/vnd.jupyter.widget-state+json">
               // widget state
           </script>

       </head>

       <body>
           <h1>GMaps embedding example</h1>
           <div id="widget-embedded-here">
               <script type="application/vnd.jupyter.widget-view+json">
               {
                   "model_id": "c05e9b0ca0dd405295d2adde29776c95"
               }
               </script>
           </div>
       </body>
   </html>


