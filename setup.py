#!/usr/bin/env python

import sys
import os


REQUIRED_PYTHON = (3, 10)
CURRENT_PYTHON = sys.version_info[:2]

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of Regex-Toolkit requires at least Python {}.{}, but you're trying to install it on Python {}.{}.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

here = os.path.abspath(os.path.dirname(__file__))

# Legacy install
from setuptools import setup

setup()
