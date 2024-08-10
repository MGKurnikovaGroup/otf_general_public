#!/bin/bash

# for X in "$@"
# do
# 	cp -r $X "$X"_1
#         cp -r $X "$X"_2
# 	mv $X "$X"_0
# done

# if [ $# -lt 2 ]; then
#     echo "Usage: $0 num_copies dir1 [dir2 ... dirN]"
#     exit 1
# fi

num_copies=$1

shift

# Loop through each directory
for X in "$@"
do
    # Loop to create the specified number of copies
    for ((i=1; i<=num_copies; i++))
    do
        cp -r "$X" "${X}_$i"
    done
    # Rename the original directory/file
    mv "$X" "${X}_0"
done