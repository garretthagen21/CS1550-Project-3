#!/bin/sh
if [ -d submission ]
then rm -r submission
fi

mkdir submission
cp CS1550-Project-3-WriteUp.pdf submission/
cp *.py submission/
mv submission/vmsim.py submission/vmsim


