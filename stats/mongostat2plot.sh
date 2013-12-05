#!/bin/bash

if [[ $# -eq 0 || -z $1 || ! -f $1 ]]; then
   echo "Provide an exosting mongostat file as parameter"
fi

./mongostat_sane --gb2mb --stripdb < $1 > $1.csv
sed -e "s/%FILE%/$1/g" ./template.gnuplot > $1.gnuplot
./makeplot.sh $1.csv
