#!/usr/bin/env python

from distutils.core import setup

import gmaps
version = gmaps.__version__

setup(name="gmaps",
      version=version,
      description="IPython plugin for Google Maps JavaScript API",
      author="Pascal Bugnion",
      author_email="pascal@bugnion.org",
      packages=["gmaps"]
)
