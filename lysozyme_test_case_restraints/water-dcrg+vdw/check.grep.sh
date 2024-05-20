#!/bin/bash

grep '_wt' */*/*in
echo -----------------------------
grep 'maxcyc' */1*/*in
echo -----------------------------
grep 'nstlim' */3*/1*in
echo -----------------------------
grep 'nstlim' */prod/*in

