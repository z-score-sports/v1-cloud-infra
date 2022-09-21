#!/bin/bash
mkdir shared
python -m pipenv requirements > shared/requirements.txt
pip install -r shared/requirements.txt -t shared/python --upgrade