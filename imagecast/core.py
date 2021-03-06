# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import io

from PIL import Image
from requests_cache import CachedSession


class ImageEngine:

    http = None

    def __init__(self, cache_ttl=300):
        self.data = None
        self.image = None
        self.format = None

        # Setup HTTP client cache
        if ImageEngine.http is None:
            ImageEngine.http = CachedSession(backend="memory", expire_after=cache_ttl)

    def download(self, uri):
        response = self.http.get(uri)
        self.data = response.content

    def read(self):
        self.image = Image.open(io.BytesIO(self.data))
        self.format = self.image.format

    def monochrome(self, threshold):

        # self.image = self.image.convert('1')
        # self.image = self.image.convert('1', dither=False)

        fn = lambda x: 255 if x > threshold else 0
        self.image = self.image.convert("L").point(fn, mode="1")

    def grayscale(self):
        self.image = self.image.convert("L")

    def resize_width(self, width):
        size = self.image.size
        wpercent = width / float(size[0])
        height = int((float(size[1]) * float(wpercent)))
        self.image = self.image.resize((width, height), resample=Image.ANTIALIAS)

    def resize_height(self, height):
        size = self.image.size
        hpercent = height / float(size[1])
        width = int((float(size[0]) * float(hpercent)))
        self.image = self.image.resize((width, height), resample=Image.ANTIALIAS)

    def crop(self, box):
        size = self.image.size
        (left, top, right, bottom) = box
        if right < 0:
            right = size[0] + right
        if bottom < 0:
            bottom = size[1] + bottom
        box = (left, top, right, bottom)
        self.image = self.image.crop(box)

    def display(self):
        self.image.show()

    def to_bytes(self):
        return self.image.tobytes()

    def to_buffer(self, format, dpi):
        buffer = io.BytesIO()
        self.image.save(buffer, format=format, dpi=(dpi, dpi))
        return buffer.getvalue()


def process(options):
    ie = ImageEngine(cache_ttl=options.cache_ttl)
    ie.download(options.uri)
    ie.read()

    if options.monochrome:
        ie.monochrome(int(options.monochrome))

    if options.grayscale:
        ie.grayscale()

    # (left, top, right, bottom)
    if options.crop:
        cropbox = map(int, options.crop.split(","))
        ie.crop(cropbox)

    if options.width:
        ie.resize_width(int(options.width))
    if options.height:
        ie.resize_height(int(options.height))

    return ie
