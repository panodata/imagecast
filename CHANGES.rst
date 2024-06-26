###################
Imagecast changelog
###################


in progress
===========

2024-04-15 0.7.0
================
- Added software tests for HTTP API and CLI
- Fixed HTTP API by downgrading to pydantic 1.x
- Removed support for Python 3.7
- Upgrade to pydantic-settings

2023-12-20 0.6.0
================
- Add capability to acquire images from HTML web pages, and elements thereof
- Remove support for Python 3.6
- Add support for Python 3.12


2023-01-17 0.5.0
================
- Update dependencies across the board
- Add support for Python 3.10 and 3.11


2021-03-06 0.4.0
================
- Add explicit ``--reload`` option to ``imagecast service`` for development mode
- Get rid of the "httptools" dependency
- Store the image format for later reuse directly after reading the original image
- Run black and isort on the code base
- Improve dependencies
- Improve documentation
- Add software tests


2020-06-08 0.3.0
================
- Use static response instead of streaming response aka. ``Transfer-Encoding: chunked``
- Improve HTTP caching


2020-06-08 0.2.0
================
- Add HTTP API


2020-06-06 0.1.1
================
- Update slogan


2020-06-06 0.1.0
================
- First version, with command line interface
