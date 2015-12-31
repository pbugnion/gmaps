
# Provides a compatibility layer between different versions of IPython

import IPython
ipy_version = IPython.version_info[0]

if IPython.version_info[0] == 2:
    raise ValueError("gmaps works with IPython version 3.0 or later")
