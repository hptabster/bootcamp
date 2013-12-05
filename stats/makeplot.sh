#!/bin/bash -e

FILE=$(basename $1)
FILENAME="${FILE%.*}"

rm -f   $FILENAME.png
gnuplot $FILENAME.gnuplot
open    $FILENAME.png
