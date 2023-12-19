import sys

import PIL
import pytest

from imagecast.core import ImageEngine


@pytest.fixture
def ie() -> ImageEngine:
    ie = ImageEngine()

    # Acquire image.
    ie.download("https://unsplash.com/photos/WvdKljW55rM/download?force=true")

    return ie


def test_read(ie: ImageEngine):

    assert ie.data.startswith(
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01"
    )
    assert ie.image is None

    # Read image.
    ie.read()
    assert isinstance(ie.image, PIL.JpegImagePlugin.JpegImageFile)
    assert ie.format == "JPEG"

    # Test some original image attributes.
    assert ie.image.getbbox() == (0, 0, 3024, 4032)
    assert ie.image.getbands() == ("R", "G", "B")
    assert ie.image.getextrema() == ((0, 255), (0, 255), (0, 255))
    assert ie.image.getpalette() is None
    assert round(ie.image.entropy(), 2) == 8.32


def test_grayscale(ie: ImageEngine):

    ie.read()
    ie.grayscale()

    assert ie.image.getbbox() == (0, 0, 3024, 4032)
    assert ie.image.getbands() == ("L",)
    assert ie.image.getextrema() == (0, 255)
    assert ie.image.getpalette() is None
    assert round(ie.image.entropy()) == 7


def test_monochrome(ie: ImageEngine):

    ie.read()
    ie.monochrome(50)

    assert ie.image.getbbox() == (0, 0, 3024, 4032)
    assert ie.image.getbands() == ("1",)
    assert ie.image.getextrema() == (0, 255)
    assert ie.image.getpalette() is None
    assert round(ie.image.entropy(), 2) == 0.45


def test_crop(ie: ImageEngine):

    ie.read()
    ie.crop((50, 50, 200, 200))

    assert ie.image.getbbox() == (0, 0, 150, 150)
    assert round(ie.image.entropy()) == 8


def test_resize_width(ie: ImageEngine):

    ie.read()
    ie.resize_width(320)

    assert ie.image.getbbox() == (0, 0, 320, 426)
    assert round(ie.image.entropy()) == 8


def test_resize_height(ie: ImageEngine):

    ie.read()
    ie.resize_height(400)

    assert ie.image.getbbox() == (0, 0, 300, 400)
    assert round(ie.image.entropy()) == 8


def test_to_buffer(ie: ImageEngine):

    ie.read()
    ie.crop((50, 50, 100, 100))
    buffer = ie.to_buffer("png", dpi=72)

    assert buffer.startswith(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")


def test_to_bytes(ie: ImageEngine):

    ie.read()
    ie.crop((50, 50, 100, 100))
    buffer = ie.to_bytes()

    assert False \
        or buffer.startswith(b"\x80") \
        or buffer.startswith(b"\x7f") \
        or buffer.startswith(b"{")
