#!/usr/bin/env python

"""
Run a web server displaying the current documentation.
The server reloads when there are changes to the source.

This requires the livereload module
(https://github.com/lepture/python-livereload/).

Run from this directory:
$ python run_dev.py
"""

from livereload import Server, shell

PORT = '8080'
BUILD = shell('make html', cwd='.')

server = Server()
server.watch('source/*', BUILD)
server.watch('../gmaps/', BUILD)
server.serve(root='build/html', port=PORT)
