#!/bin/bash

DIR=$1

cp --parents vdw*/prod/*sh $DIR
cp --parents vdw*/prod/*in $DIR

cp *prmtop *inpcrd *RST *sh $DIR

