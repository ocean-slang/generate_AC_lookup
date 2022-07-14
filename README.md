# generate_AC_lookup
Generate look up table for atmospheric correction using Py6S and 6S radiative transfer model. All open source

Written by Sarah Lang from University of RI


thank you to Mollie Passacantando (URI, https://web.uri.edu/gso/meet/mollie-m-passacantando/) for python help and Yulun Wu (https://yulunwu8.github.io/) for recommending this procedure

Download Py6s: https://py6s.readthedocs.io/en/latest/index.html

documentation: https://py6s.readthedocs.io/_/downloads/en/stable/pdf/

for those new to python:

you need anaconda or miniconda3, create new environment for py6s. see more in the Py6s documentation at link above.

I run my code through the command line like this:

source /Users/sarahlang/miniconda3/bin/activate py6s-env #activate your environment
cd /Volumes/slangSSD #set cd to be where your script is located
python3 generateLU.py #run with python
