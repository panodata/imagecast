.. image:: https://img.shields.io/badge/Python-3-green.svg
    :target: https://github.com/panodata/imagecast

.. image:: https://img.shields.io/pypi/v/imagecast.svg
    :target: https://pypi.org/project/imagecast/

.. image:: https://img.shields.io/github/tag/panodata/imagecast.svg
    :target: https://github.com/panodata/imagecast

|

.. imagecast-readme:

#########
Imagecast
#########


*****
About
*****
Imagecast is like ImageMagick but for Pythonistas.
Optionally provides its features via HTTP API.

Currently, this is based on Pillow_. However, it
might be based on Wand_ in the future.

There might still be dragons.

.. _Pillow: https://pillow.readthedocs.io/
.. _Wand: http://wand-py.org/


*******
Install
*******

Prerequisites
=============
::

    pip install imagecast

With service API::

    pip install imagecast[service]


********
Features
********
- Colorspace conversion: monochrome, grayscale
- Cropping with negative right/bottom padding
- Resizing while keeping aspect ratio
- Output format: Any image formats or bytes
- HTTP API


********
Synopsis
********
::

    # Display on screen
    imagecast --uri="$IMGURL" --display

    # Colorspace reduction to bi-level with threshold, output as bytes
    imagecast --uri="$IMGURL" --monochrome=200 --format=bytes

    # Colorspace reduction, cropping, resizing and format conversion
    imagecast --uri="$IMGURL" --grayscale --crop=40,50,-50,-40 --width=200 --save=test.png


Example::

    imagecast --uri="https://unsplash.com/photos/WvdKljW55rM/download?force=true" --monochrome=80 --crop=850,1925,-950,-900 --width=640 --display


HTTP API
========
Start the Imagecast service as daemon::

    imagecast service

Example::

    /?uri=https%3A%2F%2Funsplash.com%2Fphotos%2FWvdKljW55rM%2Fdownload%3Fforce%3Dtrue&monochrome=80&crop=850,1925,-950,-900&width=640
