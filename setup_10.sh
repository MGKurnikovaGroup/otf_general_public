#!/bin/bash

for X in "$@"
do
	cp -r $X "$X"_1
        cp -r $X "$X"_2
	cp -r $X "$X"_3
	cp -r $X "$X"_4
	cp -r $X "$X"_5
	cp -r $X "$X"_6
	cp -r $X "$X"_7
	cp -r $X "$X"_8
	cp -r $X "$X"_9
	mv $X "$X"_0
done
