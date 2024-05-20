#!/bin/bash

PRMTOP_NAME=$1
REF_NAME=$2
TRG_NAME=$3
OUT_NAME=$4

cpptraj -p ${PRMTOP_NAME} <<_EOF
reference ${REF_NAME}
trajin ${TRG_NAME}
rmsd @CA reference out ${OUT_NAME}.rmsdca.dat
trajout ${OUT_NAME}.rst7
run
_EOF
