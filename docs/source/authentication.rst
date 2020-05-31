
Authentication
^^^^^^^^^^^^^^

Most operations on Google Maps require that you tell Google who you are. To authenticate with Google Maps, follow the `instructions <https://console.developers.google.com/flows/enableapi?apiid=maps_backend,geocoding_backend,directions_backend,distance_matrix_backend,elevation_backend&keyType=CLIENT_SIDE&reusekey=true>`_ for creating an API key. You will probably want to create a new project, then click on the `Credentials` section and create a `Browser key`. The API key is a string that starts with the letters ``AI``.

.. image:: _images/api_key.*

You can pass this key to `gmaps` with the ``configure`` method. Maps and layers created after the call to ``gmaps.configure`` will have access to the API key.

However, you should avoid hard-coding the API key into your Jupyter notebooks. You can use  `environment variables <https://en.wikipedia.org/wiki/Environment_variable>`_. Add the following line to your shell start-up file (probably `~/.profile` or `~/.bashrc`)::

  export GOOGLE_API_KEY=AI...

Make sure you don't put spaces around the ``=`` sign. If you then open a `new` terminal window and type ``env`` at the command prompt, you should see that your API key. Start a new Jupyter notebook server in a new terminal, and type::

  import os
  import gmaps

  gmaps.configure(api_key=os.environ["GOOGLE_API_KEY"])

If you get a "this page can't load Google maps correctly" error in your Jupyter Notebook, review the tips provided at the webpage linked from the "do you own this website" text provided in the error message; for example, you may not have properly configured billing for the GCP project associated with the API.
