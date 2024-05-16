#!/bin/bash

for X in "$@"
do
	cp -r $X "$X"_1
        cp -r $X "$X"_2
	mv $X "$X"_0
done
