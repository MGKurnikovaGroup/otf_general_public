#!/bin/bash
mywd=$(pwd)
mypcl=~/protocols/lys_abfe_10

for X in "$@"
do
        echo =====  $X  =======================
        cd $X/

        ../prep-input.sh $mypcl
        ../prep-input-water.sh $mypcl

        cd $mywd
done
