#!/bin/bash

COUNT=0

while [ $? -eq 0 ]
do
	COUNT=$[$COUNT + 1]
	echo $COUNT
	printf '=%.0s' {1..COUNT} > data.txt
	./sort data.txt
done

echo "Offset: $COUNT"
