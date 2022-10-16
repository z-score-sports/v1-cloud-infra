#!/bin/bash
mkdir shared
Copy-Item requirements.txt -Destination shared
pip install -r shared/requirements.txt -t shared/python