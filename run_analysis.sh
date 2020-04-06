#!/bin/bash

# declare variables
OUTPUT_DIR=csvfiles
TRACE_DIR=traces

# Make output directory if it doesnt exist
if [ ! -d $OUTPUT_DIR ]
then
mkdir $OUTPUT_DIR
fi

# Our parameters
frame_counts=( 8 16 32 64 )
algorithms=( lru second opt )
trace_files=( gzip swim gcc )

# Iterate through files
for file in "${trace_files[@]}"
do
	for count in "${frame_counts[@]}"
    do

	    for algo in "${algorithms[@]}"
        do
            # Run for gzip.trace
            ./vmsim.py -n $count -a $algo -d 1 -c $OUTPUT_DIR/$file.csv $TRACE_DIR/$file.trace
        done
    done
done

echo "**************** Done With Analysis **********************"