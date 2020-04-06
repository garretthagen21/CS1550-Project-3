#!/bin/sh
if [ -d submission]
then rm -rf submission
fi

mkdir submission

cp vsim.py submission/vsim
cp -r algorithms submission/algorithms

gzip GBH8-CS1550-Project-3.zip submission/