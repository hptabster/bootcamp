#!/bin/bash
p=`pwd`
pushd /tmp
split -l 20000 $p/release /tmp/release
popd
for i in /tmp/release[a-Z]*
do
  echo "./process_one_release.sh $i >> $i.log 2>&1 &"
  nohup ./process_one_release.sh $i >> $i.log 2>&1 &
done
