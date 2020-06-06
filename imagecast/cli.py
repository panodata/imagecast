# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import sys
import json
import logging

from docopt import docopt, DocoptExit

from imagecast import __appname__, __version__
from imagecast.core import ImageEngine
from imagecast.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    Imagecast modifies images, optionally serving them via HTTP API.

    Usage:
      imagecast --uri=<uri> [--monochrome=<threshold>] [--grayscale] [--width=<width>] [--height=<height>] [--crop=<cropbox>] [--display] [--format=<format>] [--dpi=<dpi>] [--save=<save>]
      imagecast service [--listen=<listen>]
      imagecast --version
      imagecast (-h | --help)

    Options:
      --uri=<uri>                       URI to image
      --monochrome=<threshold>          Make image monochrome (bi-level)
      --grayscale                       Make image grayscale
      --width=<width>                   Resize image to given width
      --height=<height>                 Resize image to given height
      --crop=<cropbox>                  Crop image to (left,top,right,bottom)
      --display                         Display image
      --format=<format>                 Output format
      --dpi=<dpi>                       Output DPI. [Default: 72]
      --save=<save>                     Path to output file
      --listen=<listen>                 HTTP server listen address. [Default: localhost:9999]
      --version                         Show version information
      --debug                           Enable debug messages
      -h --help                         Show this screen

    Examples::

    """

    name = f'{__appname__} {__version__}'

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=name))

    # Setup logging
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Debugging
    log.debug('Options: {}'.format(json.dumps(options, indent=4)))

    # Run service.
    if options.service:
        listen_address = options.listen
        log.info(f'Starting {name}')
        log.info(f'Starting web service on {listen_address}')
        from imagecast.api import start_service
        start_service(listen_address)
        return

    # Run command.

    if not (options.display or options.save or options.format):
        raise KeyError('Please specify one of "--display", "--save" or "--format"')

    ie = ImageEngine()
    ie.download(options.uri)
    ie.read()

    if options.monochrome:
        ie.monochrome(int(options.monochrome))

    if options.grayscale:
        ie.grayscale()

    # (left, top, right, bottom)
    if options.crop:
        cropbox = map(int, options.crop.split(','))
        ie.crop(cropbox)

    if options.width:
        ie.resize_width(int(options.width))
    if options.height:
        ie.resize_height(int(options.height))

    dpi = int(options.dpi)

    if options.display:
        ie.display()
    elif options.save:
        ie.image.save(options.save, dpi=(dpi, dpi))
    elif options.format:
        if options.format == 'bytes':
            buffer = ie.to_bytes()
        else:
            buffer = ie.to_buffer(options.format, dpi)
        sys.stdout.buffer.write(buffer)
