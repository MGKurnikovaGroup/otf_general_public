#!/bin/bash

DIR=$1

mkdir $DIR

cp --parents vdw*/*sh $DIR 
cp --parents vdw*/prod/*sh $DIR
cp --parents vdw*/eq*/*/*in $DIR
cp --parents vdw*/prod/*in $DIR

cp *prmtop *inpcrd *RST *sh $DIR

