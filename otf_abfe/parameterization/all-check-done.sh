#!/bin/bash

myargs=()

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -d|--directory)
                mydir="$2"; shift; shift ;;
        *)
                myargs+="$1 " # save arg
                echo -n "  $1"; shift ;;
    esac
done

echo
echo "Directory to move files: $mydir"
mkdir $mydir

for X in $myargs
do
        #echo =====  $X  =======================
        mycheck=0
        for mdextension in prmtop inpcrd
        do
                if [ -s $X/md-complex/complex.$mdextension ]
                then
                        let "mycheck+=1"
                        echo " DONE: $X/md-complex/complex.$mdextension exists and is not empty "
                else
                        echo " ERROR: $X/md-complex/complex.$mdextension file does NOT exist, or is EMPTY "
                fi
        done
        echo $X  :  $mycheck
        if [[ "$mycheck" -eq 2 ]]; then
                mv $X $mydir
                echo "moving  $X  to  $mydir"
        fi

done
