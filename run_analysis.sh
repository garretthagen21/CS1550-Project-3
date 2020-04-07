#!/bin/bash

# For fun
START_TIME=date

echo "**************** Starting Analysis **********************"

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
algorithms=( second lru opt )
trace_files=( gzip swim gcc mcf twolf )

# Iterate through files
for file in "${trace_files[@]}"
do
	 for algo in "${algorithms[@]}"
     do
        for count in "${frame_counts[@]}"
        do
            ./vmsim.py -n $count -a $algo -d 1 -c "$OUTPUT_DIR/$file-basic.csv" $TRACE_DIR/$file.trace
        done
    done
done

echo "**************** Done With All Algorithm Analysis **********************"


for file in "${trace_files[@]}"
do
    for algo in "${algorithms[@]}"
    do
        for ((i=2;i<=200;i+=2));
        do
            ./vmsim.py -n $i -a $algo -d 1 -c "$OUTPUT_DIR/$file-extensive.csv" "$TRACE_DIR/$file.trace"
        done
    done
done


echo "**************** Done With Extensive Analysis **********************"

END_TIME=date
ELAPSED_TIME=$END_TIME-$START_TIME

echo " Process took total time of $ELAPSED_TIME seconds "