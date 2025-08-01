#!/bin/bash
# Install the Python package via setuptools into the conda build prefix
$PYTHON setup.py install --single-version-externally-managed --record=record.txt

