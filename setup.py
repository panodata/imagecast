# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

setup(name="imagecast",
      version="0.6.0",
      description="Imagecast is like ImageMagick but for Pythonistas. Optionally provides its features via HTTP API.",
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author="Andreas Motl",
      author_email="andreas.motl@panodata.org",
      url="https://github.com/panodata/imagecast",
      keywords="image conversion http api proxy",
      packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      install_requires=[
          "docopt>=0.6,<1",
          "munch>=2.3,<5",
          "Pillow>=8,<11",
          "playwright<1.42",
          "requests>=2.23,<3",
          "requests-cache>=0.5,<2",
      ],
      extras_require={
          "service": [
              "fastapi<0.110",
              "uvicorn<0.28",
          ],
      },
      entry_points={
          "console_scripts": [
              "imagecast = imagecast.cli:run",
          ],
      },
)
