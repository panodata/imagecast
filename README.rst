#########
Imagecast
#########

|

.. start-badges

|ci-tests| |ci-coverage| |license| |pypi-downloads|
|python-versions| |status| |pypi-version|

.. |ci-tests| image:: https://github.com/panodata/imagecast/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/panodata/imagecast/actions/workflows/tests.yml

.. |ci-coverage| image:: https://codecov.io/gh/panodata/imagecast/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/panodata/imagecast
    :alt: Test suite code coverage

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/imagecast.svg
    :target: https://python.org

.. |pypi-version| image:: https://img.shields.io/pypi/v/imagecast.svg
    :target: https://pypi.org/project/imagecast/

.. |status| image:: https://img.shields.io/pypi/status/imagecast.svg
    :target: https://pypi.org/project/imagecast/

.. |license| image:: https://img.shields.io/pypi/l/imagecast.svg
    :target: https://pypi.org/project/imagecast/

.. |pypi-downloads| image:: https://static.pepy.tech/badge/imagecast/month
    :target: https://pepy.tech/project/imagecast

.. end-badges


*****
About
*****

Imagecast is like ImageMagick but for Pythonistas. Optionally provides its
features via HTTP API.

Currently, this is based on Pillow_. However, it might be based on Wand_ in
the future.

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
- Cropping with negative right/bottom offsets
- Resizing while keeping aspect ratio
- Output format: Any image formats from Pillow or raw bytes
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


HTML Capturing
==============

Imagecast can also capture screenshots of webpages, or elements thereof. It uses
`Playwright`_ and `Firefox`_ to convert full pages or specific DOM elements
to bitmaps.

After installing Imagecast, run::

    playwright install firefox

Then, invoke Imagecast like::

    imagecast --uri="${URL}" --display

In order to select specific elements for capturing, use the ``--element`` option
to express a DOM selector to apply::

    imagecast --uri="${URL}" --element="#panel-1" --display


HTTP API
========

Start the Imagecast service as daemon::

    imagecast service

Example::

    http "localhost:9999/?uri=https%3A%2F%2Funsplash.com%2Fphotos%2FWvdKljW55rM%2Fdownload%3Fforce%3Dtrue&monochrome=80&crop=850,1925,-950,-900&width=640"

.. note::

    You should not run the service without restricting the
    list of allowed remote hosts on the public internet.

    To do that, invoke the service like::

        imagecast service --allowed-hosts=unsplash.com,media.example.org

    By default, no host will be allowed. If you really need to enable access
    to all upstream hosts, use ``--allowed-hosts=*``. All host names must be
    listed explicitly, wildcard notations like ``*.iana.org`` are not permitted.


**************
Other projects
**************

- https://github.com/DictGet/ecce-homo
- https://github.com/agschwender/pilbox
- https://github.com/francescortiz/image


.. _Firefox: https://www.mozilla.org/firefox/
.. _Playwright: https://playwright.dev/
