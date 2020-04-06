#!/bin/sh
if [ -d submission ]
then rm -r submission
fi

mkdir submission

cp *.py submission/
mv submission/vmsim.py submission/vmsim


