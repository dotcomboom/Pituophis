#!/usr/bin/env bash

# pdoc
pdoc --html pituophis --html-dir docs/ --overwrite

# sphinx
cd sphinx
make html