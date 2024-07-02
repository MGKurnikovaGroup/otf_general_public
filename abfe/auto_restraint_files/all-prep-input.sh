#!/bin/bash
mywd=$(pwd)
mypcl=~/protocols/gp_auto_protocol

for X in "$@"
do
        echo =====  $X  =======================
        cd $X/

        ../prep-input.sh $mypcl
        ../prep-input-water.sh $mypcl

        cd $mywd
done
